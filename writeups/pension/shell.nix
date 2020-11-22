{ pkgs ? import <nixpkgs> {} }:

let pkg =
{ buildPythonPackage, requests, beautifulsoup4 }:

buildPythonPackage {
  name = "pension";

  propagatedBuildInputs = [ requests beautifulsoup4 ];
};

in pkgs.python3.pkgs.callPackage pkg { }
