#!/usr/bin/perl -w

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
    $in_count{"$correct_1 $correct_2"}{$in_length}++;
    $out_count{"$correct_1 $correct_2"}{$out_length}++;
}
close IFILE;

print "IN STATS\n";

print "by performance type\n";

foreach $performance_type (sort (keys %in_count)) {
    print $performance_type,"\n";
    foreach $length (sort { $a <=> $b } (keys %{$in_count{$performance_type}})) {
	print join("\t",($length,$in_count{$performance_type}{$length},$in_count{$performance_type}{$length}/$tot_in_count{$length})),"\n";
    }
}

print "by length\n";

foreach $length (sort { $a <=> $b } (keys %tot_in_count)) {
    print $length;
    foreach $performance_type (sort (keys %in_count)) {
	if (!defined($in_count{$performance_type}{$length})) {
	    $count_by_performance_type = 0;
	}
	else {
	    $count_by_performance_type = $in_count{$performance_type}{$length};
	}
	print "\t", join ("\t",($performance_type,$count_by_performance_type,$count_by_performance_type/$tot_in_count{$length}));
    }
    print "\n";
}

print "OUT STATS\n";

print "by performance type\n";

foreach $performance_type (sort (keys %out_count)) {
    print $performance_type,"\n";
    foreach $length (sort { $a <=> $b } (keys %{$out_count{$performance_type}})) {
	print join("\t",($length,$out_count{$performance_type}{$length},$out_count{$performance_type}{$length}/$tot_out_count{$length})),"\n";
    }
}

print "by length\n";

foreach $length (sort { $a <=> $b } (keys %tot_out_count)) {
    print $length;
    foreach $performance_type (sort (keys %out_count)) {
	if (!defined($out_count{$performance_type}{$length})) {
	    $count_by_performance_type = 0;
	}
	else {
	    $count_by_performance_type = $out_count{$performance_type}{$length};
	}
	print "\t", join ("\t",($performance_type,$count_by_performance_type,$count_by_performance_type/$tot_out_count{$length}));
    }
    print "\n";
}
