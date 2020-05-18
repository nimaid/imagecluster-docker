@echo off

call conda activate imagecluster_build
call pyinstaller ^
     --noconfirm ^
     --onedir ^
     --debug all ^
     --hidden-import="sklearn.utils._cython_blas" ^
     --hidden-import="matplotlib._mathtext_data" ^
     image-cluster.spec

call conda deactivate