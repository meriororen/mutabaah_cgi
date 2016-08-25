#!/usr/bin/perl -w
use CGI qw(:standard);
use CGI::Carp qw/fatalsToBrowser/;
use strict;
use warnings;

use Path::Tiny qw(path);

#print header('application/json');
print header('text/html');
my $response = "";
my $valid = 1;
my $user = "";
my $filename = "";
my $numarg = 9; # actual number of arguments (date + data)
my @arglist = ("user", "update","date","SJ","SR", "WQ", "SD", "ZS", "ZP", "SM", "PS");

sub dienice {
	print "ERROR! ";
	print @_;
	print ". filename: ", $filename;
	exit;
}

sub checkexist {
	return (-e $filename);	
}

sub getparam {
	my $n = 0;
	$user = param('user') ;
	$filename = $user . ".csv";
	foreach my $p (param()) { $n++; }
	if ( $n != $#arglist+1 ) { $valid = 0; }
	foreach my $p (param()) {
		if ($p ne 'update' && $p ne 'user') {  # change here also if arglist changed
			$response .= param($p);
			if ($n-- > $#arglist - $numarg + 2) { $response .= ","; }
		}
	}
	if ($filename eq ".csv") { $valid = 0; }
	return $valid;
}

sub jsonify {
	my $ret = 0;
	my @token = split(/,/, $response);
	if ( $valid == 1 ) {
		$response = '{ "status" : "OK",';
		for (my $i = 0; $i < $numarg ; $i++) {
			$response .= '"' . $arglist[$i + $#arglist - $numarg + 1] . '" : "' . $token[$i] . '"';
			if ( $i < $#token  )  { $response .= ','; }
		}
		$response .= ' }';
	} else {
		$response = '{ "status" : "NO" }';
		$ret = 1;
	}

	return $ret;
}

sub search_and_update {
	my $ret = 0;
	my $found = "";
	if (!(-e $filename)) {
		open(IN, ">>", $filename) or &dienice("Couldn't create input file: $!");
		close(IN);
		return 0;
	} else {
		open(IN, "<", $filename) or &dienice("Couldn't open input file: $!");
		my $pard = param('date');
		my $pat = qr/^$pard/;
		while(<IN>) {
			if ($_ =~ /${pat}/) {
				$found = $_;					
				$ret = 1;
				last;
			}
		}
		close(IN);
	}
	if ($ret == 1 && $valid == 1) {
		if (param('update') == 1) {
			my $file = path($filename);
			my $data = $file->slurp_utf8;
			$data =~ s/$found/${response}\n/g;
			$file->spew_utf8($data);
		} else {
			$response = $found;
		}
	}
	return $ret;
}

sub insert {
	open(OUT, ">>", $filename) or &dienice("Couldn't open output file: $!");
	print OUT $response;
	print OUT "\n";
	close(OUT);
}

sub dbg {
	open(OUT, ">>dbg.csv") or &dienice("Couldn't open output file: $!");
	print OUT $response;
	print OUT "\n";
	close(OUT);
}

getparam();
if (search_and_update() == 0) {
	if ($valid == 1) { insert(); }
} 
jsonify();
print $response, "\n";
