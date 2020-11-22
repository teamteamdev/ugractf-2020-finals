{ pkgs ? import <nixpkgs> {} }:

let pkg =
{ buildPythonPackage, flask, flask_wtf, filelock }:

buildPythonPackage {
  name = "pension";

  propagatedBuildInputs = [ flask flask_wtf filelock ];
};

in pkgs.python3.pkgs.callPackage pkg { }
