{ nixpkgs ? import <nixpkgs> {} }:
let
  inherit (nixpkgs) pkgs;
  inherit (pkgs) python38Packages;

in
pkgs.mkShell {
  buildInputs = with pkgs; [
    sqlitebrowser

    python38Packages.SPARQLWrapper
  ];
}
