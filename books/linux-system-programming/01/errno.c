#include <stdio.h>
#include <errno.h>

int main (void) {
  FILE *stream;
  printf("%d", errno);
  return 0;
}
