#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

struct Measurement {
        int sample_number;
        long long latency;
};

int main() {
	
	
        struct timespec start_time, end_time;
        long long elapsed_time;
        bool myBool = false;
		
        struct timespec final_start_time, final_end_time;
        clock_gettime(CLOCK_MONOTONIC, &final_start_time);
		
		
		
        const int num_samples = 3073;
        struct Measurement results[num_samples];



        for (int i = 0; i < num_samples; i++) {
        clock_gettime(CLOCK_MONOTONIC, &start_time);
        ///////////////////////////////////////

        myBool=true;
        myBool=false;
        myBool=true;
        myBool=false;
        myBool=true;
        myBool=false;
        myBool=true;
        myBool=false;


        ///////////////////////////////////////
        clock_gettime(CLOCK_MONOTONIC, &end_time);
        elapsed_time = (end_time.tv_sec - start_time.tv_sec) * 1e9 + (end_time.tv_nsec - start_time.tv_nsec);

        results[i].sample_number = i;
        results[i].latency = elapsed_time;
        printf("Sample %d: %lld ns\n", results[i].sample_number, results[i].latency);
        }
		
		
        clock_gettime(CLOCK_MONOTONIC, &final_end_time);

        // Save results
        //FILE *fptr = fopen("/home/test/output.txt", "w");
        FILE *fptr = fopen("output.txt", "w");

        for (int i = 1; i < num_samples; i++) {
                fprintf(fptr, "%d\n", (results[i].latency-results[i-1].latency));
        }

        fclose(fptr);
		
		
		// Save final time 
		
        elapsed_time = (final_end_time.tv_sec - final_start_time.tv_sec) * 1e9 + (final_end_time.tv_nsec - final_start_time.tv_nsec);
		FILE *time_fptr = fopen("time.txt", "w");

		fprintf(time_fptr, "%d\n", elapsed_time);

        fclose(time_fptr);
		

        return 0;
}
