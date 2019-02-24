#!/usr/bin/perl -w

$outcome_index = shift;

while (<>) {
    chomp;
    @F = split "\t",$_;
    @words = split " ",$F[0];
    foreach $word (@words) {
	$tot_count{$word}++;
	$tot_count{"TOT"}++;
	if ($F[$outcome_index] eq "True") {
	    $true_count{$word}++;
	    $true_count{"TOT"}++;
	}
    }
}
foreach $word (sort (keys %tot_count)) {
    if (!defined($true_count{$word})) {
	$true_count{$word} = 0;
    }
    print join("\t",($word,$true_count{$word},$true_count{$word}/$tot_count{$word},$tot_count{$word})),"\n";
}
