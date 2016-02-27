#include <Python.h>
#include <stdio.h>
#include <stdint.h>

static const int64_t
	K   = 2862933555777941757L;

static const double
	D   = 0x1.0p31;

int32_t guava(int64_t state, int32_t buckets) {
	double next_double;
	int32_t candidate = 0;
	int32_t next;
	while (1) {
		state = K * state + 1;
		next_double = (double)( (int32_t)( (uint64_t) state >> 33 ) + 1 ) / D;
		next = (int32_t) ( (candidate + 1) / next_double );

		if ( ( next >= 0 ) && ( next < buckets ) ) {
			candidate = next;
		} else {
			return candidate;
		}
	}
}


PyObject* py_guava(PyObject* self, PyObject* args, PyObject *keywds) {
    long state;
    int buckets;
    int64_t guava_state;
    int32_t guava_buckets;
    int32_t guava_hash_result;

    static char *kwlist[] = {"state", "buckets", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "li", kwlist,
                                     &state, &buckets)) {
        return NULL;
    }

    guava_state = (int64_t) state;
    guava_buckets = (int32_t) buckets;

    guava_hash_result = guava(guava_state, guava_buckets);

    return Py_BuildValue("i", (int) guava_hash_result);
}


struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

static PyMethodDef guavahash_funcs[] = {
    { "guava", (PyCFunction) py_guava, METH_VARARGS | METH_KEYWORDS, NULL },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3

static int guavahash_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int guavahash_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef guavahash_module = {
        PyModuleDef_HEAD_INIT,
        "guavahash",
        NULL,
        sizeof(struct module_state),
        guavahash_funcs,
        NULL,
        guavahash_traverse,
        guavahash_clear,
        NULL
};

#define INITERROR return NULL

PyObject *PyInit_guavahash(void)

#else
#define INITERROR return

void initguavahash(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&guavahash_module);
#else
    PyObject *module = Py_InitModule("guavahash", guavahash_funcs);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
