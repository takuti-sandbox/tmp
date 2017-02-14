#include <stdio.h>
#include <unistd.h>

int main(void) {
  char *params[] = {"vi", "hoge.txt", NULL};
  int ret;

  ret = execvp("vi", params);
  if (ret == -1)
    perror("execvp");

  return 0;
}
