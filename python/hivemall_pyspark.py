import os
import sys
import pandas as pd


def create_spark_session(jarname):
    try:
        from pyspark.sql import SparkSession

        path_spark = os.path.join(os.path.dirname(os.path.abspath(__file__)), jarname)

        return SparkSession.builder.master('local[*]').config('spark.jars', path_spark).enableHiveSupport().getOrCreate()
    except ImportError:
        raise RuntimeError('PySpark is not installed')
    except Exception as e:
        raise RuntimeError('failed to connect to hivemall-spark: ' + e)


def main():
    jarname = sys.argv[1]
    spark = create_spark_session(jarname)

    spark.sql("CREATE TEMPORARY FUNCTION hivemall_version AS 'hivemall.HivemallVersionUDF'")
    df_version = spark.sql("SELECT hivemall_version()")
    df_version.show()

    # preprocessing
    spark.sql("CREATE TEMPORARY FUNCTION categorical_features AS 'hivemall.ftvec.trans.CategoricalFeaturesUDF'")
    spark.sql("CREATE TEMPORARY FUNCTION quantitative_features AS 'hivemall.ftvec.trans.QuantitativeFeaturesUDF'")
    spark.sql("CREATE TEMPORARY FUNCTION array_concat AS 'hivemall.tools.array.ArrayConcatUDF'")

    # training
    spark.sql("CREATE TEMPORARY FUNCTION train_classifier AS 'hivemall.classifier.GeneralClassifierUDTF'")

    # prediction and evaluation
    spark.sql("CREATE TEMPORARY FUNCTION sigmoid AS 'hivemall.tools.math.SigmoidGenericUDF'")
    spark.sql("CREATE TEMPORARY FUNCTION extract_feature AS 'hivemall.ftvec.ExtractFeatureUDFWrapper'")
    spark.sql("CREATE TEMPORARY FUNCTION extract_weight AS 'hivemall.ftvec.ExtractWeightUDFWrapper'")
    spark.sql("CREATE TEMPORARY FUNCTION logloss AS 'hivemall.evaluation.LogarithmicLossUDAF'")
    spark.sql("CREATE TEMPORARY FUNCTION auc AS 'hivemall.evaluation.AUCUDAF'")

    # from pyspark.sql.types import StructType, StructField
    # from pyspark.sql.types import DoubleType, IntegerType, StringType
    #
    # schema = StructType([
    #     StructField("A", IntegerType()),
    #     StructField("B", DoubleType()),
    #     StructField("C", StringType())
    # ])
    # df = spark.read.option('header', True).schema(schema).csv('/Users/kitazawa/data/churn.csv')
    df = spark.createDataFrame(pd.read_csv('/Users/kitazawa/data/churn.csv'))
    df.printSchema()
    df_train, df_test = df.randomSplit([0.8, 0.2], seed=31)
    print(df_train.count(), df_test.count())

    df_train.createOrReplaceTempView('train')
    spark.sql("""
    CREATE OR REPLACE TEMPORARY VIEW train AS
    SELECT
      array_concat(
        categorical_features(
          array('intl_plan', 'vmail_plan'),
          intl_plan, vmail_plan
        ),
        quantitative_features(
          array('custserv_calls', 'account_length'),
          custserv_calls, account_length
        )
      ) as features,
      if(churn = 'True.', 1, 0) as label
    FROM
      train
    """)

    df_model = spark.sql("""
    SELECT
      feature, avg(weight) as weight
    FROM (
      SELECT
        train_classifier(features, label) as (feature, weight)
      FROM
        train
    ) t
    GROUP BY 1
    """)
    df_model.show()

    df_test.createOrReplaceTempView('test')
    spark.sql("""
    CREATE OR REPLACE TEMPORARY VIEW test AS
    SELECT
      phone,
      label,
      extract_feature(fv) AS feature,
      extract_weight(fv) AS value
    FROM (
      SELECT
        phone,
        array_concat(
          categorical_features(
            array('intl_plan', 'vmail_plan'),
            intl_plan, vmail_plan
          ),
          quantitative_features(
            array('custserv_calls', 'account_length'),
            custserv_calls, account_length
          )
        ) as features,
        if(churn = 'True.', 1, 0) as label
      FROM
        test
    ) t1
    LATERAL VIEW explode(features) t2 AS fv
    """)

    df_model.createOrReplaceTempView('model')
    df_prediction = spark.sql("""
    SELECT
      phone,
      label as expected,
      sigmoid(sum(weight * value)) as prob
    FROM
      test t LEFT OUTER JOIN model m
      ON t.feature = m.feature
    GROUP BY 1, 2
    """)
    df_prediction.show()

    df_prediction.createOrReplaceTempView('prediction')
    df_eval = spark.sql("""
    SELECT
      sum(IF(IF(prob >= 0.5, 1, 0) = expected, 1.0, 0.0)) / count(1) AS accuracy,
      auc(prob, expected) AS auc,
      logloss(prob, expected) AS logloss
    FROM (
      SELECT prob, expected
      FROM prediction
      ORDER BY prob DESC
    ) t
    """)
    df_eval.show()


if __name__ == '__main__':
    main()
