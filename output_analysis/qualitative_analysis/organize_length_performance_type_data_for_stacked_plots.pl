#!/usr/bin/perl -w

$in_or_out = shift;
$file_name = shift;

# initializing variables that are used only once for the time being,
# to avoid variable-used-once warnings
$out_1 = "";
$out_2 = "";

open IFILE,$file_name;
while (<IFILE>) {
    chomp;
    ($in,$out_1,$out_2,$correct_1,$correct_2,$out_gold) = split "\t",$_;
    @temp_units = split (" ",$in);
    $in_length = $#temp_units + 1;
    @temp_units = split (" ",$out_gold);
    $out_length = $#temp_units + 1;
    $tot_in_count{$in_length}++;
    $tot_out_count{$out_length}++;
    $in_count{$correct_1 . "_" . $correct_2}{$in_length}++;
    $out_count{$correct_1 . "_" . $correct_2}{$out_length}++;
}
close IFILE;

if ($in_or_out eq "in") {
    @performance_types = sort (keys %in_count);
    foreach $length (sort { $a <=> $b } (keys %tot_in_count)) {
	push @lengths,$length;
	foreach $performance_type (@performance_types) {
	    if (!defined($in_count{$performance_type}{$length})) {
		$count_by_performance_type = 0;
	    }
	    else {
		$count_by_performance_type = $in_count{$performance_type}{$length};
	    }
	    push @{$normalized_cases_count{$performance_type}},$count_by_performance_type/$tot_in_count{$length};
	}
    }
}
elsif ($in_or_out eq "out") {
    @performance_types = sort (keys %out_count);
    foreach $length (sort { $a <=> $b } (keys %tot_out_count)) {
	push @lengths,$length;
	foreach $performance_type (@performance_types) {
	    if (!defined($out_count{$performance_type}{$length})) {
		$count_by_performance_type = 0;
	    }
	    else {
		$count_by_performance_type = $out_count{$performance_type}{$length};
	    }
	    push @{$normalized_cases_count{$performance_type}},$count_by_performance_type/$tot_out_count{$length};
	}
    }
}
else {
    die "first argument must be in or out\n";
}


#print join("\t",("L",@performance_types)),"\n";;

$i=0;
while ($i<=$#lengths) {
    print $lengths[$i];
    foreach $performance_type (@performance_types) {
	print "\t",$normalized_cases_count{$performance_type}[$i];
    }
    print "\n";
    $i++;
}

