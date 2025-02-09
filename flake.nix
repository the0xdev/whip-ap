{
  description = "my eternally W.I.P ActivityPub server.";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        runpkg = pkg: "${pkgs.${pkg}}/bin/${pkg}";
        runpypkg = pkg: "${pkgs.python312Packages.${pkg}}/bin/${pkg}";
        runpy = pkg: "${pkgs.${pkg}}/bin/python";
      in
        with pkgs;
        let
          name = "whip-ap";
          src = ./.;
          buildInputs = with python312Packages; [
            django
          ];

          nativeBuildInputs = with python312Packages; [
          ];
          
        in {
          packages = rec {
            default = prod;

            prod = stdenv.mkDerivation {
              inherit name src buildInputs nativeBuildInputs;

              buildPhase = ''

              '';
              installPhase = ''
                cp -r public $out
              '';
            };
          };
          apps = let
            template = ''${runpy "python312"} manage.py runserver'';

            dev-server = pkgs.writeShellScriptBin "dev-server" template;
          in rec {
            default = dev;

            dev = flake-utils.lib.mkApp {
              drv = dev-server;
            };

            test = flake-utils.lib.mkApp {
              
            };
          };
        }
    );
}
