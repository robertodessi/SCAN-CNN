#!/usr/bin/perl -w

# out format:
# word absolute_count_false proportion absolute_count_true proportion absolute_count

while (<>) {
    # skip meta-data footer
    if (/^[ ]*\|/) {
	next;
    }
    chomp;
    @F = split "\t",$_;
    @words = split " ",$F[0];
    foreach $word (@words) {
	$count_in{$F[3]}{$word}++;
	$count_tot{$word}++;
    }
}

foreach $word (sort keys %count_tot) {
    print $word;
    for $truth_value (sort keys %count_in) {
	if (!defined($count_in{$truth_value}{$word})) {
	    $absolute_in = 0;
	}
	else {
	    $absolute_in = $count_in{$truth_value}{$word};
	}
	print "\t",$absolute_in,"\t",$absolute_in/$count_tot{$word};
    }
    print "\t",$count_tot{$word},"\n";
}

	
	
