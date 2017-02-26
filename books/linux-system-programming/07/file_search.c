#include <stdio.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <string.h>

int find_file_in_dir(char *path, char *file) {
  struct dirent *entry;
  int ret = 1;
  DIR *dir;

  dir = opendir(path);

  errno = 0;
  while ((entry = readdir(dir)) != NULL) {
    if (!strcmp(entry->d_name, file)) {
      ret = 0;
      break;
    }
  }

  if (errno && !entry)
    perror("readdir");

  closedir(dir);
  return ret;
}

int main(void) {
  char *path = "/Users/takuti";
  char *file = "foo.txt";

  if (!find_file_in_dir(path, file))
    printf("Found!\n");
  else
    printf("Not found...\n");

  return 0;
}
