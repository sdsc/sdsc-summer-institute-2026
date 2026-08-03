#include <cstdint>
#include <stdexcept>
#include <cstdio>
#include <cstdlib>
#include <math.h>
#include <time.h>

class Matrix {
public:
  // C order...dim[1] contiguous (row)
  double * const data;  // buffer owned by this object
  size_t dims[2];

  Matrix() = delete;

  Matrix(size_t _n_cols, size_t _n_rows)
    : data(new double[_n_cols*_n_rows]),
      dims{_n_cols,_n_rows} {}

  ~Matrix() { delete[] data; }

  // We do not allow copy constructors and assignments, to avoid accidental copies
  Matrix(const Matrix &) = delete;
  Matrix &operator=(const Matrix &) = delete;

  // But allow the move
  Matrix(Matrix &&) = default;

  constexpr size_t els() const {return dims[0]*dims[1];}
  constexpr size_t n_cols() const {return dims[0];}
  constexpr size_t n_rows() const {return dims[1];}

  // indexes are 0-based
  constexpr size_t get_row_idx(size_t col) const { return col*dims[1];}
  constexpr size_t get_el_idx(size_t col, size_t row) const { return get_row_idx(col)+row;}

  constexpr double& el(size_t col, size_t row) {return data[get_el_idx(col,row)];}
  constexpr double el(size_t col, size_t row) const {return data[get_el_idx(col,row)];}

  Matrix operator*(double c) const {
    Matrix out(dims[0],dims[1]);
#pragma omp parallel for
    for (size_t col=0; col<dims[0]; col++)
      for (size_t row=0; row<dims[1]; row++)
        out.el(col,row) = el(col,row)*c;
    return out;
  }

  Matrix operator+(double c) const {
    Matrix out(dims[0],dims[1]);
#pragma omp parallel for
    for (size_t col=0; col<dims[0]; col++)
      for (size_t row=0; row<dims[1]; row++)
        out.el(col,row) = el(col,row)+c;
    return out;
  }

  Matrix operator-(double c) const {
    Matrix out(dims[0],dims[1]);
#pragma omp parallel for
    for (size_t col=0; col<dims[0]; col++)
      for (size_t row=0; row<dims[1]; row++)
        out.el(col,row) = el(col,row)-c;
    return out;
  }

  Matrix operator*(const Matrix &other) const {
    Matrix out(dims[0],dims[1]);
    if ((other.dims[0] == dims[0]) &&
         (other.dims[1] == dims[1])) {
         // same size, multiply all elements
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)*other.el(col,row);
    } else {
      throw std::runtime_error("Dims mismatch");
    }
    return out;
  }

  Matrix operator+(const Matrix &other) const {
    Matrix out(dims[0],dims[1]);
    if (other.dims[0] == dims[0]) {
       if (other.dims[1] == dims[1]) {
         // same size, add all elements
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)+other.el(col,row);
       } else if (other.dims[1]==1) {
         // add the only element to all the rows in each column
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)+other.el(col,0);
       } else {
         throw std::runtime_error("Row mismatch");
       }
    } else if (other.dims[0]==1) {
       if (other.dims[1] == dims[1]) {
         // add the only element to all the rows in each column
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)+other.el(0,row);
       } else {
         throw std::runtime_error("Row mismatch");
       }
    } else {
      throw std::runtime_error("Col mismatch");
    }
    return out;
  }

  Matrix operator-(const Matrix &other) const {
    Matrix out(dims[0],dims[1]);
    if (other.dims[0] == dims[0]) {
       if (other.dims[1] == dims[1]) {
         // same size, subtract all elements
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)-other.el(col,row);
       } else if (other.dims[1]==1) {
         // subtract the only element to all the rows in each column
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)-other.el(col,0);
       } else {
         throw std::runtime_error("Row mismatch");
       }
    } else if (other.dims[0]==1) {
       if (other.dims[1] == dims[1]) {
         // subtract the only element to all the rows in each column
#pragma omp parallel for
         for (size_t col=0; col<dims[0]; col++)
           for (size_t row=0; row<dims[1]; row++)
             out.el(col,row) = el(col,row)-other.el(0,row);
       } else {
         throw std::runtime_error("Row mismatch");
       }
    } else {
      throw std::runtime_error("Col mismatch");
    }
    return out;
  }

  double mean() const {
    double sum = 0.0;
#pragma omp parallel for reduction(+:sum)
    for (size_t col=0; col<dims[0]; col++)
      for (size_t row=0; row<dims[1]; row++)
         sum+=el(col,row);
     return sum/els();
  }

  Matrix col_means() const {
    Matrix out(dims[0],1);
#pragma omp parallel for
    for (size_t col=0; col<dims[0]; col++) {
      double sum = 0.0;
      for (size_t row=0; row<dims[1]; row++)
         sum+=el(col,row);
      out.el(col,0) = sum/dims[1];
    }
    return out;
  }

  Matrix row_means() const {
    Matrix out(1,dims[1]);
#pragma omp parallel for
    for (size_t row=0; row<dims[1]; row++) {
      double sum = 0.0;
      for (size_t col=0; col<dims[0]; col++)
         sum+=el(col,row);
      out.el(0,row) = sum/dims[0];
    }
    return out;
  }

};

// TODO: Optimize memory access
double centre_mean(Matrix &m) {
   Matrix m1 = m*m*(-0.5);
   Matrix m2 = m1-m1.row_means()-m1.col_means()+m1.mean();
   return m2.mean();
}

// Default values if no command line arguments are provided
#define DEFAULT_VECTOR_SIZE 1600
#define DEFAULT_ITERATIONS 100

int main(int argc, char *argv[]) {
    int N = DEFAULT_VECTOR_SIZE;
    int iterations = DEFAULT_ITERATIONS;

    // Parse command line arguments if provided
    if (argc >= 2) {
        N = atoi(argv[1]);
        if (N <= 0) N = DEFAULT_VECTOR_SIZE;
    }
    if (argc >= 3) {
        iterations = atoi(argv[2]);
        if (iterations <= 0) iterations = DEFAULT_ITERATIONS;
    }

    Matrix m1(N,N);
#pragma omp parallel for
    for (int col=0; col<N; col++)
      for (int row=0; row<N; row++)
        m1.el(col,row) = 0.1*col-0.15*row;

    struct timespec start_real, end_real;
    // Start timing
    timespec_get(&start_real, TIME_UTC);

    // keep something to output, to avoid over-optimization
    double o = 0;
    for (int i=0; i<iterations; i++) {
      o+=centre_mean(m1);
      // just change one element to avoid over-optimization
      m1.data[i%N]+=1;
    }

    // End timing
    timespec_get(&end_real, TIME_UTC);
    double real_time = (end_real.tv_sec - start_real.tv_sec) +
                       (end_real.tv_nsec - start_real.tv_nsec) / 1e9;

    printf("Total time: %f, result %f\n",real_time,o);
    return 0;
}
