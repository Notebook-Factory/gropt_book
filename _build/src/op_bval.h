#ifndef CVX_OPBVAL_H
#define CVX_OPBVAL_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "cvx_matrix.h"

typedef struct {
    int active;
    int verbose;
    
    int N;
    int ind_inv;
    double dt;

    double weight;
    double mat_norm;

    cvx_mat sigBdenom;
    cvx_mat sigB;

    cvx_mat csx;
    cvx_mat Btau;
    cvx_mat C;
    
    cvx_mat zB;
    cvx_mat zBbuff;
    cvx_mat zBbar;
    cvx_mat Bx;
    
    // Used for CG
    cvx_mat b;
    cvx_mat x;
    cvx_mat r;
    cvx_mat p;
    cvx_mat Ap;

} cvxop_bval;

void cvxop_bval_init(cvxop_bval *opB, int N, int ind_inv, double dt, double init_weight, int verbose);
void cvxop_bval_updatesigma(cvxop_bval *opB);
void cvxop_bval_reweight(cvxop_bval *opB, double weight_mod);
void cvxop_bval_add2tau(cvxop_bval *opB, cvx_mat *tau_mat);
void cvxop_bval_add2taumx(cvxop_bval *opB, cvx_mat *taumx);
void cvxop_bval_update(cvxop_bval *opB, cvx_mat *txmx, double relax, double *ddebug, int count);
void cvxop_bval_destroy(cvxop_bval *opB);

void cvxop_bval_prox(cvxop_bval *opB);
void cvxop_bval_proxxbar(cvxop_bval *opB, cvx_mat *xbar, double eps);



#endif /* CVX_OPBVAL_H */