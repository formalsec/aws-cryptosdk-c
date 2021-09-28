#include "assert.h"

int __logor(int a, int b) {
  return a || b;
}

int __logand(int a, int b) {
  return a && b;
}

void exit (int e) { assert(1); }
void __assert_fail(const char *id, const char *file,
    unsigned int i, const char *func) {
  assert(0);
}
int __VERIFIER_nondet_bool(char *name) {
  int sym_var = sym_int(name);
  return sym_var;
}
char __VERIFIER_nondet_char(char *name) { 
  int sym_var = sym_int(name);
  return sym_var & 0x000000ff;
}
unsigned char __VERIFIER_nondet_uchar(char *name) { 
  int sym_var = sym_int(name);
  return sym_var & 0x000000ffU;
}
short __VERIFIER_nondet_short(char *name) { 
  int sym_var = sym_int(name);
  return sym_var & 0x0000ffff;
}
unsigned short __VERIFIER_nondet_ushort(char *name) { 
  int sym_var = sym_int(name);
  return sym_var & 0x0000ffffU;
}

int __VERIFIER_nondet_int(char *name) { return sym_int(name); }

unsigned int __VERIFIER_nondet_uint(char *name) { 
  unsigned int sym_var = sym_int(name);
  return sym_var;
}

unsigned int __VERIFIER_nondet_charp(char *name) { return sym_int(name); }

int __VERIFIER_nondet_long(char *name) { return sym_long(name); }

unsigned int __VERIFIER_nondet_ulong(char *name) { 
  int sym_var = sym_long(name);
  return sym_var;
}

float __VERIFIER_nondet_float(char *name) { return sym_float(name); }

double __VERIFIER_nondet_double(char *name) { return sym_double(name); }
