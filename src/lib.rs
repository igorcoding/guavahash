use pyo3::prelude::*;

const K: i64 = 2862933555777941757;
const D: f64 = 2147483648.0; // 0x1.0p31

fn guava_hash(mut state: i64, buckets: i32) -> i32 {
    let mut candidate = 0i32;
    
    loop {
        state = K.wrapping_mul(state).wrapping_add(1);
        let next_double = (((state as u64) >> 33) as i32).wrapping_add(1) as f64 / D;
        let next = ((candidate + 1) as f64 / next_double) as i32;
        
        if next >= 0 && next < buckets {
            candidate = next;
        } else {
            return candidate;
        }
    }
}

#[pyfunction]
fn guava(state: i64, buckets: i32) -> PyResult<i32> {
    Ok(guava_hash(state, buckets))
}

#[pymodule]
fn guavahash(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(guava, m)?)?;
    Ok(())
}