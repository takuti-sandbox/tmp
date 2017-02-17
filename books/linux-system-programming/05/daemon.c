#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

// #include <linux/fs.h>
#define NR_OPEN (1024 * 1024)

int main(void) {
  pid_t pid;
  int i;

  // create new process which will be daemon
  pid = fork();
  if (pid == -1) // error
    return -1;
  else if (pid != 0) // parent process
    exit(EXIT_SUCCESS);

  // create new session and process group
  // daemon will be a session leader
  // this doesn't have terminal window
  if (setsid() == -1)
    return -1;

  // set the working directory to the root directory
  // because daemon will stay the directory
  if (chdir("/") == -1)
    return -1;

  // close all file descriptors
  for (i = 0; i < NR_OPEN; i++)
    close(i);

  // open /dev/null as file descriptor 0, 1, 2
  open("/dev/null", O_RDWR); // stdin
  dup(0); // clone fd=0 to minimum un-opened fd (=1; stdout)
  dup(0); // clone fd=0 to minimum un-opened fd (=2; stderr)

  // do something

  return 0;
}
