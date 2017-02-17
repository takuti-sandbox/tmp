#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int my_system(char *cmd) {
  int status;
  pid_t pid;

  pid = fork();
  if (pid == -1) // error
    return -1;
  else if (pid == 0) { // child
    char *argv[4];
    argv[0] = "sh";
    argv[1] = "-c";
    argv[2] = cmd;
    argv[3] = NULL;
    execv("/bin/sh", argv);

    exit(-1); // why return -1?
  }

  // parent
  if (waitpid(pid, &status, 0) == -1)
    return -1;
  else if (WIFEXITED(status)) // normal termination
    return WEXITSTATUS(status);

  return -1;
}

int main(void) {
  my_system("echo \"Hello!\"");
  my_system("ls -al");
  return 0;
}
