img = dask-numba-si26.sif
recipe = Singularity.anaconda3-dask-numba
singularity = singularity
build_flags = --fakeroot

build: ${recipe} clean
	${singularity} build ${build_flags} ${img} ${recipe}

clean:
	rm -f ${img}

copy: ${img}
	scp ${img} expanse:/expanse/lustre/projects/sds166/zonca/
