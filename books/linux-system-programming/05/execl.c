#include <stdio.h>
#include <unistd.h>

int main(void) {
  int ret;

  // replace own process id with vi
  ret = execl("/usr/bin/vi", "vi", NULL);
  if (ret == -1)
    perror("ecxecl");

  return 0;
}
