#!/usr/bin/perl -W

# Creates a single-track workshop schedule with inline abstracts.
#
# Usage: 
#
#   cat data/WMT14/proceedings/order | order2schedule_workshop.pl WMT14
#
# Writes files to auto/NAME

use strict;

my (@S, @P, @D);
my $conf_part = $ARGV[0];	# main / wsX / demo 

my @args = @ARGV;
my $with_abstracts = 0;
my $debug = 0;
while (my $a = shift @args)
{
  if ($a =~ /^-a|--with-abstracts/)
  {
    $with_abstracts = 1;
  }
  if ($a =~ /^-d|--debug/)
  {
    $debug = 1;
  }
  else
   {
     $conf_part = $a;
   } 
}

die "Conference part tag not specified!\n" unless $conf_part;
$|=1;

my $tpat     = "[0-9]{1,2}[:.][0-9]{2,2}(?:\\s*[ap]m)?";
my $tspanpat = "\\(?($tpat)(?:\\s*-+\\s*($tpat))?\\)?";
my $daynum = 1;
while (my $line = <STDIN>) {
  next if $line =~ /^#/ or $line =~ /^\s*$/;
  $line =~ s/\r\n/\n/;
  print "\n" if ($line =~ /^[*=+]/);
  print "\% $line" if $debug;
  "a" =~ /a/; # reset match variables
  if ($line =~ /^\* (.*)/)
  {
    my $header = $1;
    $header = texify($header) if $header;
    print "\\vspace{7em}\n" if $daynum > 1;
    print"\\item[] {\\Large\\bfseries $header}\\\\\\vspace{1.5ex}\n";
    $daynum++;
  }
  elsif ($line =~ /^[=+!]\s+(.*?)($tspanpat)\s*(.*)/i)
  {
    my $pre   = $1;
    my $time  = lc($2);
    my $start = $3;
    my $end   = $4;
    my ($post,$hash) = splitkeys($5);
    $start = "" unless $start;
    $end   = "" unless $end;
    $pre  = texify($pre)  if $pre;
    $post = texify($post) if $post;
    my $author = (exists $hash->{'%by'} ? " ($hash->{'%by'})" : "");
    #print "$pre\n$post\n$start\n$end\n";
    print"\\vspace{1ex}\n";
    $time =~ s/(\d+):(\d+)/minus12($1,$2)/eg;
    print "\\item[$time] {\\bfseries $pre $post$author}\n";
  }
  elsif ($line =~ /^[=+]\s*(.*)/)
  {
    my $header = texify($1);
    print"\\vspace{1ex}\n";
    print "\\item[] {\\bfseries $header}\n";
  }
  elsif ($line =~ /^([0-9]+)\s+($tspanpat)?\s*\#/i)
  {
    my $paper_id  = $1;
    my $time = $2;
    $time = "\$\\bullet\$" unless $time;
    $time = lc($time);
    my @t;
    push @t, $3 if $3;
    push @t, $4 if $4;
    my $endsat   = scalar(@t) ? pop @t : "\$\\bullet\$";
    my $startsat = scalar(@t) ? pop @t : "";
    $time =~ s/(\d+):(\d+)/minus12($1,$2)/eg;
    print sprintf("\\item[$time] \\wspaperentry{$conf_part-%03d}\n", $paper_id);
  }
  else
  {
    print STDERR "NO MATCH FOR: $conf_part ||| $line";
  }
}

sub texify
{
  $_[0] =~ s/ "/ ``/g;
  $_[0] =~ s/" /''/g;
  # $_[0] =~ s/\\/\\\\/g;
  $_[0] =~ s/\@/\\\@/g;
  return $_[0];
}

sub minus12 {
  my ($h, $m) = @_;
  $h =~ s/^0//;
  if ($h >= 13) {
    $h -= 12;
    return "$h:$m";
  } elsif ($h == 12) {
    return "$h:$m";
  } else {
    return "$h:$m";
  }
}

sub splitkeys {
  my $str = shift;
  my $event = $str;
  $event =~ s/ %.*//;
  my %hash;
  $hash{$1} = $2 while $str =~ /(%\w+) ([^%]+)/g;
  return ($event, \%hash);
}
    
