#!/usr/bin/perl -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser/;
use strict;
use warnings;

use DateTime;

print header('application/json');
my $startd = param('start');
my $endd = param('end');
my $user = param('user');
my $data = param('data');
my $filename = $user . ".csv";
my @arresp = ();
my $response = "";

my %start;
@start{qw[day month year]} = split /_/, $startd;
my %end;
@end{qw[day month year]} = split /_/, $endd;

my $start = DateTime->new(%start);
my $end = DateTime->new(%end);

sub dienice {
	print "ERROR! ";
	print @_;
	print ". filename: ", $filename;
	exit;
}

sub getdata {
	open(my $file, '<', $filename) or &dienice("Cannot open file! $!");
	while (<$file>) {
		my %currdate;
		my @fields = split(',');
		my @d = split('_', $fields[0]);
		$currdate{'day'} = $d[0];
		$currdate{'month'} = $d[1];
		$currdate{'year'} = $d[2];
		my $_currdate = DateTime->new(%currdate);
		if ($_currdate >= $start && $_currdate <= $end) { 
			push @arresp, @fields[0,$data];
		}
	}
}

sub jsonifygraph {
	$response = "{ ";
	for(my $i = 0; $i <= $#arresp; $i += 2) {
		$response .= '"' . $arresp[$i] . '" : "' . $arresp[$i+1];
		if ($#arresp - 1 > $i) { $response .= '",'; }
	}
	$response .= '" }';
}

getdata();
jsonifygraph();
print $response;
