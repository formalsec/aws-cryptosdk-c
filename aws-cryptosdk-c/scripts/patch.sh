#!/bin/sh

TEST=$1

echo "patching $TEST"
sed -i'' -e 's/\<call $assume\>/sym_assume/' $TEST
sed -i'' -e 's/\<call $assume_abort_if_not\>/sym_assume/' $TEST
sed -i'' -e 's/\<call $assume_cycle_if_not\>/sym_assume/' $TEST
sed -i'' -e 's/\<call $assert\>/sym_assert/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_bool/b32.symbolic/' $TEST
sed -i'' -e 's/\<call $__VERIFIER_nondet_char\>/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_uchar/i32.symbolic/' $TEST
sed -i'' -e 's/call $sym_int/i32.symbolic/' $TEST
sed -i'' -e 's/call $sym_long/i64.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_short/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_ushort/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_int/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_uint/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_long/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_ulong/i32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_float/f32.symbolic/' $TEST
sed -i'' -e 's/call $__VERIFIER_nondet_double/f64.symbolic/' $TEST
sed -i'' -e 's/call $is_symbolic/is_symbolic/' $TEST
sed -i'' -e 's/\<call $alloc\>/alloc/' $TEST
sed -i'' -e 's/\<call $free\>/free/' $TEST
sed -i'' -e 's/\<call $dealloc\>/free/' $TEST
sed -i'' -e 's/(elem (;0;) (i32.const 1) func/(elem (;0;) (i32.const 1)/' $TEST
sed -i'' -e 's/anyfunc/funcref/' $TEST
sed -i'' -e 's/\<call $IFG\>/__trace_condition/' $TEST
sed -i'' -e 's/\<call $__ternary\>/__ternary_op/' $TEST
sed -i'' -e 's/\<call $__logand\>/i32.__logand/' $TEST
sed -i'' -e 's/\<call $__logor\>/i32.__logor/' $TEST
