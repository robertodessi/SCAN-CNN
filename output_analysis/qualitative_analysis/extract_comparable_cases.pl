#!/usr/bin/perl -w

use List::Util qw(shuffle);

$out_length = shift;
$right_index = shift;
if ($right_index == 3) {
    $wrong_index = 4;
}
else {
    $wrong_index = 3;
}
$length_target = shift;

$setup_1_file = shift;
$setup_2_file = shift;

open SET1,$setup_1_file;
while (<SET1>) {
    chomp;
    @F = split "\t",$_;
    if ($length_target eq "out") {
	@items = split " ",$F[$#F];
    }
    else {
	@items = split " ",$F[0];
    }
    if ($#items+1 != $out_length || $F[$right_index] ne "True" || $F[$wrong_index] ne "False") {
	next;
    }
    $right_in_first{$F[0]}++;
}
close SET1;

open SET2,$setup_2_file;
while (<SET2>) {
    chomp;
    @F = split "\t",$_;
    if (!$right_in_first{$F[0]} || $F[$right_index] ne "False" || $F[$wrong_index] ne "True") {
	next;
    }
    if ($right_index eq 3) {
	$wrong_output_of{$F[0]} = $F[1];
    }
    else {
	$wrong_output_of{$F[0]} = $F[2];
    }
    push @selected_sentences,$F[0];
}
close SET2;

#@shuffled_selected = shuffle(@selected_sentences);
foreach $sent (sort (@selected_sentences)) {
    print join("\t",($sent,$wrong_output_of{$sent})),"\n";
}


