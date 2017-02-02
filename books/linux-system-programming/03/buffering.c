#include <stdio.h>

int main(void) {
  FILE *in, *out;
  struct pirate {
    char name[100];
    unsigned long booty;
    unsigned int beard_len;
  } p, blackbeard = { "Edward Teach", 950, 48 };

  if (!(out = fopen("data", "w"))) {
    perror("fopen");
    return 1;
  }

  if (!fwrite(&blackbeard, sizeof(struct pirate), 1, out)) {
    perror("fwite");
    return 1;
  }

  if (fclose(out)) {
    perror("fclose");
    return 1;
  }

  if(!(in = fopen("data", "r"))) {
    perror("fopen");
    return 1;
  }

  if (!fread(&p, sizeof(struct pirate), 1, in)) {
    perror("fread");
    return 1;
  }

  if (fclose(in)) {
    perror("fclose");
    return 1;
  }

  printf("name = %s, booty = %lu, beard_len = %u\n", p.name, p.booty, p.beard_len);

  return 0;
}
