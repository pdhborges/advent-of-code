#include <stdio.h>
#include <math.h>

int main (int argc, char const *argv[])
{
	long long a = 1, b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0;
	
	b = (84 * 100) + 100000;
	c = b + 17000;
	do { 
		f = 1;
		d = 2;
		
		// optimize primality test
		long long sqrtb = ((long long) sqrt(b)) + 1;
		for (d = 2; d <= sqrtb; d++) {
			if (b % d == 0) {
				f = 0;
			}
		}
	
		if (f == 0) {
			h++;
		}
		if (b == c) {
			break;
		}
		b += 17;
	} while (1);
	
	printf("%lld\n", h);
	
	return 0;
}