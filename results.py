import pstats
p = pstats.Stats('profile_result.prof')
p.sort_stats('cumulative').print_stats(10)  # This will print the top 10 functions where most of the time was spent
