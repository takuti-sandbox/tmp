#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(void) {
  pid_t pid;

  pid = fork();
  if (pid == -1)
    perror("fork");

  if (pid > 0) {
    printf("My baby pid=%d will execute `vi`!\n", pid);
  } else if (!pid) {
    char *params[] = {"vi", "foo.txt", NULL};
    int ret;

    ret = execvp("vi", params);
    if (ret == -1) {
      perror("execvp");
      exit(EXIT_FAILURE);
    }
  }

  return 0;
}
