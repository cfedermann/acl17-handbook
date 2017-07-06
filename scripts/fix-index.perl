#!/usr/bin/perl -W

# This script makes sorting work correctly with makeindex, which doesn't sort
# unicode correctly. This works using a feature of makeindex that permits you
# to specify a different key from the display text in the form 
#
# \indexentry{KEY@TEXT}

use strict;

while (my $line = <STDIN>)
{
  $line =~ /\\indexentry{(.*)}{([^{}]+)}\s*$/;
  my $a = $1;  # name
  my $p = $2;  # pageref
  my $s = $a;  # name
  $s =~ s/\\IeC //g;
  $s =~ s/\\[^[:alpha:]]//g;
  $s =~ s/ }//g;
  $s =~ s/~/ /g;
  $s =~ s/[^[:alpha:], ~-]//g;
  print "\\indexentry{$s\@$a}{$p}\n";
}
