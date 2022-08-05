#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct sqlite3 sqlite3;
int sqlite3_open(const char *filename, sqlite3 **ppDb);
int sqlite3_exec(sqlite3*, const char *sql, int (*callback)(void*,int,char**,char**), void *, char **errmsg);
int sqlite3_rekey( sqlite3 *db, const void *pKey, int nKey);
int sqlite3_key( sqlite3 *db, const void *pKey, int nKey);

int main(int argc, char **argv){

    if (argc < 2)
    {
        printf("[!] %s filename key\n", *argv);
        return 1;
    }

    sqlite3* db;
    int ret;

    const char *filename = *++argv;
    const char *pKey = *++argv;

    if (strlen(pKey) != 16)
    {
        printf("[-] Key:%s length is not 16\n", pKey);
        return 1;
    }

    printf("[+] filename: %s  pKey: %s\n", filename, pKey);


    ret = sqlite3_open(filename, &db);
    printf("[+] QQ sqlite3_open  %d \n", ret);

    ret = sqlite3_key(db, pKey, 16);
    printf("[+] QQ sqlite3_key %d \n", ret);
    
    char *zErrMsg = 0;
    
    ret = sqlite3_exec(db, "select name from sqlite_master where type='ttable';", 0, 0, &zErrMsg);
    printf("[+] QQ sqlite3_exec %d - %s\n", ret, zErrMsg);
    
    ret = sqlite3_rekey(db, "", 0);
    printf("[+] QQ sqlite3_rekey %d \n", ret);

    return 0;
}
