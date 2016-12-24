#include <stdio.h>
#include <stdlib.h> 
#include "pwnable_harness.h"

void win(void) {
	char flag[64];
	
	FILE* fp = fopen("flag.txt", "r");
	if(!fp) {
		puts("error, contact admin");
		exit(0);
	}
	
	fgets(flag, sizeof(flag), fp);
	fclose(fp);
	puts(flag);
}

void handle_connection(int sock) {
	int correct = 0;
	char bof[64];
	
	scanf("%s", bof);
	
	if(correct != 0xdeadbeef) {
		puts("you suck!");
		exit(0);
	}
	
	win();
}


int main(int argc, char** argv) {
	/* Defaults: Run on port 9001 for 30 seconds as user "ctf_bof2" in a chroot */
	server_options opts = {
		.user = "ctf_bof2",
		.chrooted = true,
		.port = 9001,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
