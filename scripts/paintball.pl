#!/usr/bin/env perl
use strict;
use warnings;

if (@ARGV < 2) {
    die "Usage: $0 <rotations> <step_angle>\nExample: $0 10 1\n";
}

my ($max_rotations, $step_angle) = @ARGV;

my $max_degrees = $max_rotations * 360;
my @buckets = (0) x 360;
my $current_degrees = 0;

while (1) {
    $current_degrees += $step_angle;
    last if $current_degrees > $max_degrees;
    $buckets[$current_degrees % 360]++;
}

print "Angular Distribution Matrix (18 Rows x 20 Columns):\n";
print "-" x 80 . "\n";

for (my $row = 0; $row < 18; $row++) {
    my @row_values;
    for (my $col = 0; $col < 20; $col++) {
        my $index = ($row * 20) + $col;
        push @row_values, $buckets[$index];
    }
    print join(' ', map { sprintf("%4d", $_) } @row_values) . "\n";
}
print "-" x 80 . "\n";

