use pyo3::prelude::*;

#[pyfunction]
fn add_numbers(a: i64, b: i64) -> PyResult<i64> {
    Ok(a + b)
}

#[pymodule]
fn optimizer_core(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_numbers, m)?)?;
    Ok(())
}