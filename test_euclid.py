from __future__ import division, print_function, unicode_literals

import copy
import io
from math import sqrt, sin, cos, radians, degrees, hypot
try:
    import cPickle as pickle
except Exception:
    import pickle
import unittest

import euclid as eu

fe = 1.0e-5

class Test_Vector2(unittest.TestCase):
    def test_instantiate(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)
        self.assertEqual((v.x, v.y), a)

    def test_instantiate_default(self):
        v = eu.Vector2()
        self.assertEqual((v.x, v.y), (0, 0))

    def test_copy(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)

        copied = v.__copy__()
        self.assertEqual((v.x, v.y), (copied.x, copied.y))
        self.assertFalse(copied is v)

    def test_deepcopy(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)

        copied = copy.deepcopy(v)
        self.assertEqual((v.x, v.y), (copied.x, copied.y))
        self.assertFalse(copied is v)
        self.assertFalse(hasattr(copied, '__dict__'))

    # they need __getstate__  and  __setstate__  implemented
    def test_pickle_lower_protocols(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)

        s = pickle.dumps(v, 0)
        copied = pickle.loads(s)
        self.assertEqual((v.x, v.y), (copied.x, copied.y))
        self.assertFalse(copied is v)        
        self.assertFalse(hasattr(copied, '__dict__'))

        s = pickle.dumps(v, 1)
        copied = pickle.loads(s)
        self.assertEqual((v.x, v.y), (copied.x, copied.y))
        self.assertFalse(copied is v)        
        self.assertFalse(hasattr(copied, '__dict__'))

    # don't need __getstate__ / __setstate__ implemented 
    def test_pickle_protocol_2(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)

        s = pickle.dumps(v, 2)
        copied = pickle.loads(s)
        self.assertEqual((v.x, v.y), (copied.x, copied.y))
        self.assertFalse(copied is v)        
        self.assertFalse(hasattr(copied, '__dict__'))

    def test_eq_v2(self):
        a = (1.0, 2.0)
        self.assertTrue(eu.Vector2(*a), eu.Vector2(*a))

        other = (1.0, 3.0)
        self.assertTrue( eu.Vector2(*a) != eu.Vector2(*other))

    def test_eq_tuple(self):
        a = (1.0, 2.0)
        self.assertEqual(eu.Vector2(*a), a)

        other = (1.0, 2.0, 3.0)
        self.assertRaises( AssertionError,
                           lambda r, s: r == s, eu.Vector2(*a), other)

        other = 1.0
        self.assertRaises( AssertionError,
                           lambda r, s: r == s, eu.Vector2(*a), other)

    def test_if_vector(self):
        v = eu.Vector2(0.0, 0.0)
        if v:
            eval_true = True
        else:
            eval_true = False
        self.assertFalse(eval_true)

        v = eu.Vector2(1.0, 0.0)
        if v:
            eval_true = True
        else:
            eval_true = False
        self.assertTrue(eval_true)

        v = eu.Vector2(0.0, 1.0)
        if v:
            eval_true = True
        else:
            eval_true = False
        self.assertTrue(eval_true)

        v = eu.Vector2(1.0, 1.0)
        if v:
            eval_true = True
        else:
            eval_true = False
        self.assertTrue(eval_true)

    def test_len(self):
        a = (1.0, 2.0)
        self.assertEqual(len(eu.Vector2(*a)), 2)
        
    def test_index_access__get(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)
        self.assertEqual( v[0], a[0])
        self.assertEqual(v[1], a[1])
        self.assertRaises(IndexError,
                          lambda u: v[u], 2)

    def test_index_access__set(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)
        v[0] = 7.0
        self.assertEqual((v.x, v.y), (7.0, 2.0))
        v[1] = 8.0
        self.assertEqual((v.x, v.y), (7.0, 8.0))
        def f():
            v[2] = 9.0 
        self.assertRaises(IndexError, f)

    def test_iter(self):
        a = [1.0, 2.0]
        v = eu.Vector2(*a)
        sequence = [e for e in v]
        self.assertEqual(sequence, a)
        
    def test_swizzle_get(self):
        a = (1.0, 2.0)
        v = eu.Vector2(*a)
        self.assertEqual(v.x, a[0])
        self.assertEqual(v.y, a[1])
        self.assertEqual(v.xy, a)
        self.assertEqual(v.yx, (a[1], a[0]))

        exception = None
        try:
            v.z == 11.0
        except Exception as e:
            exception = e
        assert isinstance(exception, AttributeError)
        
    def test_sub__v2_v2(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        self.assertEqual(va-vb, eu.Vector2(2.0, 5.0))
        
    def test_sub__v2_t2(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        self.assertEqual(va-b, eu.Vector2(2.0, 5.0))

    def test_rsub__t2_v2(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        self.assertEqual(a-vb, eu.Vector2(2.0, 5.0))

    # in py3 or py2 with 'from __future__ import division'
    # else the integer division is used, as in old euclid.py
    def test_default_div(self):
        a = (4, 7)
        v = eu.Vector2(*a)

        c = v / 3
        self.assertEqual((c.x, c.y) , (4.0 / 3, 7.0 / 3))

    def test_integer_division(self):
        a = (4, 7)
        v = eu.Vector2(*a)

        c = v // 3
        self.assertEqual((c.x, c.y) , (4.0 // 3, 7.0 // 3))
    
    def test_add(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        w = va + vb

        self.assertTrue(isinstance(w, eu.Vector2))
        self.assertEqual((w.x, w.y), (4.0, 9.0))

        c = (11.0, 17.0)
        pc = eu.Point2(*c)
        d = (13.0, 23.0)
        pd = eu.Point2(*d)
        
        self.assertTrue(isinstance(va+pc, eu.Point2))
        self.assertTrue(isinstance(pc+pd, eu.Vector2))

        self.assertTrue(isinstance(va + b, eu.Vector2))
        self.assertEqual(va + vb, va + b)

    def test_inplace_add(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        va += vb
        self.assertEqual((va.x, va.y) , (4.0, 9.0))

        va = eu.Vector2(*a)
        va += b
        self.assertEqual((va.x, va.y) , (4.0, 9.0))
        
    def test_mul(self):
        a = (4.0, 7.0)
        v = eu.Vector2(*a)
        u = 2.0

        self.assertEqual( v * u, (8.0, 14.0))

    def test_imul(self):
        a = (4.0, 7.0)
        v = eu.Vector2(*a)
        v *= 2.0

        self.assertEqual( v, (8.0, 14.0))

    def neg(self):
        a = (4.0, 7.0)
        v = eu.Vector2(*a)
        w = -v

        self.assertFalse(w is v)
        self.assertTrue( (w.x, w.y), (-4.0, -7.0) )

    def test_abs(self):
        a = (3.0, 4.0)
        v = eu.Vector2(*a)

        self.assertTrue(abs(abs(v) - 5.0) < fe)

    def test_magnitude_squared(self):
        a = (3.0, 4.0)
        v = eu.Vector2(*a)
        u = abs(v)
        self.assertTrue(abs(v.magnitude_squared() - u**2) < fe)

    def test_normalize(self):
        a = (3.0, 0.0)
        v = eu.Vector2(*a)
        v.normalize()
        self.assertTrue(abs(v - eu.Vector2(*(1.0, 0.0))) < fe)

        a = (0.0, 3.0)
        v = eu.Vector2(*a)
        v.normalize()
        self.assertTrue(abs(v - eu.Vector2(*(0.0, 1.0))) < fe)

    def test_normalized(self):
        a = (3.0, 0.0)
        v = eu.Vector2(*a)
        w = v.normalized()
        self.assertFalse(w is v)
        self.assertTrue(abs(w - eu.Vector2(*(1.0, 0.0))) < fe)

        a = (0.0, 1.0)
        v = eu.Vector2(*a)
        w = v.normalized()
        self.assertFalse(w is v)
        self.assertTrue(abs(w - eu.Vector2(*(0.0, 1.0))) < fe)

    def test_dot(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        d = va.dot(vb)
        self.assertTrue(abs(d - (3.0 + 14.0)) < fe)

    def test_determinant(self):
        self.assertTrue(abs(1 - eu.Vector2(1, 0).determinant(eu.Vector2(0, 1))) < fe)
        self.assertTrue(abs(-1 - eu.Vector2(0, 1).determinant(eu.Vector2(1, 0))) < fe)
        self.assertTrue(abs(0 - eu.Vector2(0, 1).determinant(eu.Vector2(0, 1))) < fe)
        
    def test_cross(self):
        a = (3.0, 7.0)
        va = eu.Vector2(*a)
        vb = va.cross()
        self.assertEqual((vb.x, vb.y) , (7.0, -3.0))

    def test_reflect(self):
        a = (1.0, 1.0)
        v = eu.Vector2(*a)
        normal = eu.Vector2(*(1.0, 0.0))
        w = v.reflect(normal)
        self.assertFalse(w is v)
        self.assertTrue( abs(w - eu.Vector2(*(-1.0, 1.0))) < fe)
        self.assertTrue( abs(w.reflect(normal) - v) < fe )

    def test_rotate(self):
        v = eu.Vector2(1, 0)
        self.assertTrue(abs(v.rotate(radians(90)) - eu.Vector2(0, 1)) < fe)
        v = eu.Vector2(0, 1)
        self.assertTrue(abs(v.rotate(radians(90)) - eu.Vector2(-1, 0)) < fe)
        v = eu.Vector2(-1, 0)
        self.assertTrue(abs(v.rotate(radians(90)) - eu.Vector2(0, -1)) < fe)
        v = eu.Vector2(0, -1)
        self.assertTrue(abs(v.rotate(radians(90)) - eu.Vector2(1, 0)) < fe)

    def test_angle(self):
        aa = 25
        v = eu.Vector2(3.0 * cos(radians(aa)), 3.0 * sin(radians(aa)))
        bb = 35
        w = eu.Vector2(5.0 * cos(radians(bb)), 5.0 * sin(radians(bb)))
        self.assertTrue( abs(degrees(v.angle(w)) - 10.0) < fe )
        # orientation doesn't matter
        self.assertEqual(v.angle(w), w.angle(v))

    def test_angle_oriented(self):
        aa = 25
        v = eu.Vector2(3.0 * cos(radians(aa)), 3.0 * sin(radians(aa)))
        bb = 35
        w = eu.Vector2(5.0 * cos(radians(bb)), 5.0 * sin(radians(bb)))
        self.assertTrue( abs(degrees(v.angle_oriented(w)) - 10.0) < fe )
        # orientation matters
        self.assertEqual(v.angle_oriented(w), -w.angle_oriented(v))

    def test_project(self):
        aa = 25
        v = eu.Vector2(3.0 * cos(radians(aa)), 3.0 * sin(radians(aa)))
        self.assertTrue( abs(v.project(eu.Vector2(2.0, 0.0)) - v.x * eu.Vector2(1.0, 0.0)) < fe)
        self.assertTrue( abs(v.project(eu.Vector2(0.0, 5.0)) - v.y * eu.Vector2(0.0, 1.0)) < fe)
        self.assertTrue( abs(v.project(v) - abs(v) * eu.Vector2(cos(radians(aa)), sin(radians(aa)))) < fe)

class Test_Vector3(unittest.TestCase):

    def test_instantiate(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)
        self.assertEqual((v.x, v.y, v.z), a)

    def test_instantiate_default(self):
        v = eu.Vector3()
        self.assertEqual((v.x, v.y, v.z), (0, 0, 0))

    def test_copy(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)

        copied = v.__copy__()
        self.assertEqual((v.x, v.y, v.z), (copied.x, copied.y, copied.z))
        self.assertFalse(copied is v)

    def test_deepcopy(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)

        copied = copy.deepcopy(v)
        self.assertEqual((v.x, v.y, v.z), (copied.x, copied.y, copied.z))
        self.assertFalse(copied is v)        

    # they need __getstate__  and  __setstate__  implemented
    def test_pickle_lower_protocols(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)

        s = pickle.dumps(v, 0)
        copied = pickle.loads(s)
        self.assertEqual((v.x, v.y, v.z), (copied.x, copied.y, copied.z))
        self.assertFalse(copied is v)        
        self.assertFalse(hasattr(copied, '__dict__'))

        s = pickle.dumps(v, 1)
        copied = pickle.loads(s)
        self.assertEqual((v.x, v.y, v.z), (copied.x, copied.y, copied.z))
        self.assertFalse(copied is v)        
        self.assertFalse(hasattr(copied, '__dict__'))

    # no need for __getstate__ and __setstate__
    def test_pickle_protocol_2(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)

        s = pickle.dumps(v, 2)
        copied = pickle.loads(s)
        self.assertEqual((v.x, v.y, v.z), (copied.x, copied.y, copied.z))
        self.assertFalse(copied is v)        

    def test_eq_v3(self):
        a = (1.0, 2.0, 3.0)
        self.assertTrue(eu.Vector3(*a), eu.Vector3(*a))

        other = (1.0, 3.0, 7.0)
        self.assertTrue( eu.Vector3(*a) != eu.Vector3(*other))

    def test_eq_tuple(self):
        a = (1.0, 2.0, 3.0)
        self.assertEqual(eu.Vector3(*a), a)

        other = (1.0, 2.0, 3.0, 4.0)
        self.assertRaises( AssertionError,
                           lambda r, s: r == s, eu.Vector3(*a), other)

        other = 1.0
        self.assertRaises( AssertionError,
                           lambda r, s: r == s, eu.Vector3(*a), other)

    def test_if_vector(self):
        a = eu.Vector3(0.0, 0.0, 0.0)
        if a:
            eval_true = True
        else:
            eval_true = False
        self.assertFalse(eval_true)

        a = eu.Vector3(1.0, 0.0, 0.0)
        if a:
            eval_true = True
        else:
            eval_true = False
        self.assertTrue(eval_true)

        a = eu.Vector3(0.0, 2.0, 0.0)
        if a:
            eval_true = True
        else:
            eval_true = False
        self.assertTrue(eval_true)

        a = eu.Vector3(0.0, 0.0, 1.0)
        if a:
            eval_true = True
        else:
            eval_true = False
        self.assertTrue(eval_true)

    def test_len(self):
        a = (1.0, 2.0, 3.0)
        self.assertEqual(len(eu.Vector3(*a)), 3)
        
    def test_index_access__get(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)
        self.assertEqual(v[0], a[0])
        self.assertEqual(v[1], a[1])
        self.assertEqual(v[2], a[2])
        self.assertRaises(IndexError,
                          lambda u: v[u], 3)

    def test_index_access__set(self):
        a = (1.0, 2.0, 3.0)
        v = eu.Vector3(*a)
        v[0] = 7.0
        self.assertEqual((v.x, v.y, v.z), (7.0, 2.0, 3.0))
        v[1] = 8.0
        self.assertEqual((v.x, v.y, v.z), (7.0, 8.0, 3.0))
        v[2] = 9.0
        self.assertEqual((v.x, v.y, v.z), (7.0, 8.0, 9.0))
        def f():
            v[3] = 9.0 
        self.assertRaises(IndexError, f)

    def test_iter(self):
        a = [1.0, 2.0, 3.0]
        v = eu.Vector3(*a)
        sequence = [e for e in v]
        self.assertEqual(sequence, a)
        
    def test_swizzle_get(self):
        xyz = (1.0, 2.0, 3.0)
        v3 = eu.Vector3(*xyz)
        self.assertEqual(v3.x, xyz[0])
        self.assertEqual(v3.y, xyz[1])
        self.assertEqual(v3.z, xyz[2])

        self.assertEqual(v3.xy, (xyz[0], xyz[1]))
        self.assertEqual(v3.xz, (xyz[0], xyz[2]))
        self.assertEqual(v3.yz, (xyz[1], xyz[2]))

        self.assertEqual(v3.yx, (xyz[1], xyz[0]))
        self.assertEqual(v3.zx, (xyz[2], xyz[0]))
        self.assertEqual(v3.zy, (xyz[2], xyz[1]))

        self.assertEqual(v3.xyz, xyz)
        self.assertEqual(v3.xzy, (xyz[0], xyz[2], xyz[1]) )
        self.assertEqual(v3.zyx, (xyz[2], xyz[1], xyz[0]) )
        self.assertEqual(v3.zxy, (xyz[2], xyz[0], xyz[1]) )
        self.assertEqual(v3.yxz, (xyz[1], xyz[0], xyz[2]) )
        self.assertEqual(v3.yzx, (xyz[1], xyz[2], xyz[0]) )

        exception = None
        try:
            v3.u == 11.0
        except Exception as a:
            exception = a
        assert isinstance(exception, AttributeError)

    def test_sub__v3_v3(self):
        a = (3.0, 7.0, 9.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)
        self.assertTrue(isinstance(va-vb, eu.Vector3))
        self.assertEqual(va-vb, eu.Vector3(2.0, 5.0, 6.0))
        
    def test_sub__v3_p3(self):
        a = (3.0, 7.0, 9.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Point3(*b)
        self.assertTrue(isinstance(va-vb, eu.Point3))

    def test_sub__v3_t3(self):
        a = (3.0, 7.0, 9.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)
        self.assertEqual(va-b, eu.Vector3(2.0, 5.0, 6.0))

    def test_rsub__t3_v3(self):
        a = (3.0, 7.0, 9.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)
        self.assertEqual(a-vb, eu.Vector3(2.0, 5.0, 6.0))

    def test_default_div(self):
        a = (4, 7, 11)
        v = eu.Vector3(*a)

        c = v / 3
        self.assertEqual((c.x, c.y, c.z) , (4.0 / 3, 7.0 / 3, 11.0 / 3))

    def test_integer_division(self):
        a = (4, 7, 11)
        v = eu.Vector3(*a)

        c = v // 3
        self.assertEqual((c.x, c.y, c.z) , (4.0 // 3, 7.0 // 3, 11.0 // 3))
    
    def test_add(self):
        a = (3.0, 7.0, 11.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)

        self.assertTrue(isinstance(va+vb, eu.Vector3))
        self.assertEqual(repr(va+vb), 'Vector3(%.2f, %.2f, %.2f)' % (4.0, 9.0, 14.0))

        c = (13.0, 17.0, 23.0)
        pc = eu.Point3(*c)
        d = (31.0, 37.0, 41.0)
        pd = eu.Point3(*d)
        
        self.assertTrue(isinstance(va+pc, eu.Point3))
        self.assertTrue(isinstance(pc+pd, eu.Vector3))

        self.assertTrue(isinstance(va + b, eu.Vector3))
        self.assertEqual(va + vb, va + b)

    def test_inplace_add(self):
        a = (3.0, 7.0, 11.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)
        va += vb
        self.assertEqual((va.x, va.y, va.z) , (4.0, 9.0, 14.0))

        va = eu.Vector3(*a)
        va += b
        self.assertEqual((va.x, va.y, va.z) , (4.0, 9.0, 14.0))
        
    def test_mul(self):
        a = (3.0, 7.0, 11.0)
        v = eu.Vector3(*a)
        u = 2.0

        self.assertEqual( v * u, (6.0, 14.0, 22.0))

    def test_imul(self):
        a = (3.0, 7.0, 11.0)
        v = eu.Vector3(*a)
        v *= 2.0

        self.assertEqual( v, (6.0, 14.0, 22.0))

    def neg(self):
        a = (3.0, 7.0, 11.0)
        v = eu.Vector3(*a)
        w = -v

        self.assertFalse(w is v)
        self.assertTrue( (w.x, w.y, w.z), (-3.0, -7.0, -11.0) )


    def test_abs(self):
        a = (3.0, 7.0, 11.0)
        v = eu.Vector3(*a)

        self.assertTrue(abs(abs(v) - sqrt(9.0 + 49.0 + 121.0)) < fe)

    def test_magnitude_squared(self):
        a = (3.0, 7.0, 11.0)
        v = eu.Vector3(*a)
        u = abs(v)
        self.assertTrue(abs(v.magnitude_squared() - u**2) < fe)

    def test_normalize(self):
        a = (3.0, 0.0, 0.0)
        v = eu.Vector3(*a)
        v.normalize()
        self.assertTrue(abs(v - eu.Vector3(*(1.0, 0.0, 0.0))) < fe)

        a = (0.0, 3.0, 0.0)
        v = eu.Vector3(*a)
        v.normalize()
        self.assertTrue(abs(v - eu.Vector3(*(0.0, 1.0, 0.0))) < fe)

        a = (0.0, 0.0, 3.0)
        v = eu.Vector3(*a)
        v.normalize()
        self.assertTrue(abs(v - eu.Vector3(*(0.0, 0.0, 1.0))) < fe)

    def test_normalized(self):
        a = (3.0, 0.0, 0.0)
        v = eu.Vector3(*a)
        copy = v.copy()
        w = v.normalized()
        self.assertEqual(v, copy)        
        self.assertFalse(w is v)
        self.assertTrue(abs(w - eu.Vector3(*(1.0, 0.0, 0.0))) < fe)

        a = (0.0, 3.0, 0.0)
        v = eu.Vector3(*a)
        copy = v.copy()
        w = v.normalized()
        self.assertEqual(v, copy)        
        self.assertFalse(w is v)
        self.assertTrue(abs(w - eu.Vector3(*(0.0, 1.0, 0.0))) < fe)

        a = (0.0, 0.0, 3.0)
        v = eu.Vector3(*a)
        copy = v.copy()
        w = v.normalized()
        self.assertEqual(v, copy)        
        self.assertFalse(w is v)
        self.assertTrue(abs(w - eu.Vector3(*(0.0, 0.0, 1.0))) < fe)

    def test_dot(self):
        a = (3.0, 7.0, 11.0)
        b = (1.0, 2.0, 5.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)
        d = va.dot(vb)
        self.assertTrue(abs(d - (3.0 + 14.0 + 55.0)) < fe)
        
    def test_cross(self):
        xx = eu.Vector3(1.0, 0.0, 0.0)
        yy = eu.Vector3(0.0, 1.0, 0.0)
        zz = eu.Vector3(0.0, 0.0, 1.0)
        self.assertEqual(xx.cross(yy), zz)
        self.assertEqual(yy.cross(zz), xx)
        self.assertEqual(zz.cross(xx), yy)

    def test_reflect(self):
        v = eu.Vector3(1.0, 1.0, 1.0)
        w = v.reflect(eu.Vector3(1.0, 0.0, 0.0))
        self.assertFalse(w is v)
        self.assertTrue( abs(w - eu.Vector3(-1.0, 1.0, 1.0)) < fe)

        w = v.reflect(eu.Vector3(0.0, 1.0, 0.0))
        self.assertTrue( abs(w - eu.Vector3(1.0, -1.0, 1.0)) < fe)

        w = v.reflect(eu.Vector3(0.0, 0.0, 1.0))
        self.assertTrue( abs(w - eu.Vector3(1.0, 1.0, -1.0)) < fe)

    def test_rotate_around(self):
        v = eu.Vector3(3.5, 41.9, 12.7)
        axis = eu.Vector3(15.3, 22.0, 2.3)
        angle = radians(25)
        a = complex(cos(angle), sin(angle))

        # same_magnitude
        self.assertTrue( abs(abs(v)-abs(v.rotate_around(axis, angle)))<fe )

        xx = eu.Vector3(1.0, 0.0, 0.0)
        yy = eu.Vector3(0.0, 1.0, 0.0)
        zz = eu.Vector3(0.0, 0.0, 1.0)
        angle = radians(90)

        self.assertTrue( abs(xx.rotate_around(zz, angle) - yy) < fe )
        self.assertTrue( abs(xx.rotate_around(yy, angle) - (-zz)) < fe )
        self.assertTrue( abs(yy.rotate_around(zz, angle) - (-xx)) < fe )
        self.assertTrue( abs(yy.rotate_around(xx, angle) - zz) < fe )
        self.assertTrue( abs(zz.rotate_around(xx, angle) - (-yy)) < fe )
        self.assertTrue( abs(zz.rotate_around(yy, angle) - xx) < fe )

    def test_angle(self):
        aa = 25
        v = eu.Vector3(3.0 * cos(radians(aa)), 3.0 * sin(radians(aa)), 0.0)
        bb = 35
        w = eu.Vector3(5.0 * cos(radians(bb)), 5.0 * sin(radians(bb)), 0.0)
        self.assertTrue( abs(degrees(v.angle(w)) - 10.0) < fe )
        # orientation doesn't matter
        self.assertEqual(v.angle(w), w.angle(v))

        v = eu.Vector3(3.0 * cos(radians(aa)), 0.0, 3.0 * sin(radians(aa)))
        bb = 35
        w = eu.Vector3(5.0 * cos(radians(bb)), 0.0, 5.0 * sin(radians(bb)))
        self.assertTrue( abs(degrees(v.angle(w)) - 10.0) < fe )
        # orientation doesn't matter
        self.assertEqual(v.angle(w), w.angle(v))

        v = eu.Vector3(0.0, 3.0 * cos(radians(aa)), 3.0 * sin(radians(aa)))
        bb = 35
        w = eu.Vector3(0.0, 5.0 * cos(radians(bb)), 5.0 * sin(radians(bb)))
        self.assertTrue( abs(degrees(v.angle(w)) - 10.0) < fe )
        # orientation doesn't matter
        self.assertEqual(v.angle(w), w.angle(v))

    def test_project(self):
        v = eu.Vector3(1.1, 5.0, 17.3)
        x3 = eu.Vector3(3.0, 0.0, 0.0)
        y3 = eu.Vector3(0.0, 3.0, 0.0)
        z3 = eu.Vector3(0.0, 0.0, 3.0)

        self.assertTrue(abs(v.project(xx) - eu.Vector3(v.x, 0.0, 0.0)))
        self.assertTrue(abs(v.project(yy) - eu.Vector3(0.0, v.y, 0.0)))
        self.assertTrue(abs(v.project(zz) - eu.Vector3(0.0, 0.0, v.z)))

    def test_project(self):
        aa = 25
        v = eu.Vector2(3.0 * cos(radians(aa)), 3.0 * sin(radians(aa)))
        self.assertTrue( abs(v.project(eu.Vector2(2.0, 0.0)) - v.x * eu.Vector2(1.0, 0.0)) < fe)
        self.assertTrue( abs(v.project(eu.Vector2(0.0, 5.0)) - v.y * eu.Vector2(0.0, 1.0)) < fe)
        self.assertTrue( abs(v.project(v) - abs(v) * eu.Vector2(cos(radians(aa)), sin(radians(aa)))) < fe)


class Test_Point2(unittest.TestCase):
    def test_swizzle_get(self):
        xy = (1.0, 2.0)
        v2 = eu.Point2(*xy)
        self.assertEqual(v2.x, xy[0])
        self.assertEqual(v2.y, xy[1])
        self.assertEqual(v2.xy, xy)
        self.assertEqual(v2.yx, (xy[1], xy[0]))

        exception = None
        try:
            v2.z == 11.0
        except Exception as a:
            exception = a
        assert isinstance(exception, AttributeError)

# helper to assert Line2 equals
def line2_normal_rep(line):
    "norm(v) == 1, v.x>=0 if v.x !=0, else v.y <0; p with p.x==0 (if v.x!=0) or p with p.y==0"
    assert isinstance(line, eu.Line2)
    v1 = line.v.normalized()
    if v1.x < 0:
        v1 = -v1
    elif v1.x == 0 and v1.y < 0:
        v1 = -v1
    p = line.p
    if v1.x != 0:
        # choose p the point the line crosses the y-axis
        a = p.x / v1.x
        p1_x = p.x - a * v1.x
        p1_y = p.y - a * v1.y
    else:
        # choose p the point the line crosses the x-axis
        a = p.y / v1.y
        p1_x = p.x - a * v1.x
        p1_y = p.y - a * v1.y
    p1 = eu.Point2(p1_x, p1_y)
    return eu.Line2(p1, v1)

def line2_qeq(line1, line2, qe):
    "Line2 quasi equal"
    L1 = line2_normal_rep(line1)
    L2 = line2_normal_rep(line2)
    return abs(L1.p - L2.p) + abs(L1.v - L2.v) < qe

def ray2_qeq(ray1, ray2, qe):
    assert isinstance(ray1, eu.Ray2) and isinstance(ray2, eu.Ray2) 
    return abs(ray1.p - ray2.p) + abs(ray1.v.normalized() - ray2.v.normalized()) < qe

def linesegment2_qeq(ls1, ls2, qe):
    "LineSegment2 quasi equal, unoriented"
    assert isinstance(ls1, eu.LineSegment2) and isinstance(ls2, eu.LineSegment2)
    if abs(ls1.p - ls2.p) < qe:
        return abs(ls1.p - ls2.p) + abs(ls1.v - ls2.v) < qe
    q = ls1.p + ls1.v
    w = - ls1.v
    return abs(q - ls2.p) + abs(w - ls2.v) < qe

class Test_Line2_family(unittest.TestCase):
    def test_basic_sanity__linesegment2_qeq(self):
        # with itself
        a = eu.Point2(1, 2); b = eu.Point2(5, 11)
        r = eu.LineSegment2(a, b)
        self.assertTrue(linesegment2_qeq(r, r, fe))
        # with reversed
        s = eu.LineSegment2(b, a)
        self.assertTrue(linesegment2_qeq(r, s, fe))
        # with different
        b = eu.Point2(5, 11.1)
        s = eu.LineSegment2(a, b)
        self.assertFalse(linesegment2_qeq(r, s, fe))

    def test_basic_sanity__line2_qeq(self):
        ## line t*(2, 1) + (0, 1)
        a = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        # same p, same v -> True
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        self.assertTrue(line2_qeq(a, b, fe))
        # same v, different p -> False
        b = eu.Line2(eu.Point2(0.0, 1.5), eu.Vector2(2.0, 1.0))
        self.assertFalse(line2_qeq(a, b, fe))
        # non-parallel v, same p -> False
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.5))
        self.assertFalse(line2_qeq(a, b, fe))

    def test_basic_sanity__ray2_qeq(self):
        ## ray t*(2, 1) + (0, 1)
        a = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        # same p, same v -> True
        b = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        self.assertTrue(ray2_qeq(a, b, fe))
        # same v, different p -> False
        b = eu.Ray2(eu.Point2(0.0, 1.5), eu.Vector2(2.0, 1.0))
        self.assertFalse(ray2_qeq(a, b, fe))
        # non-parallel v, same p -> False
        b = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.5))
        self.assertFalse(ray2_qeq(a, b, fe))

    def test_Line2_basics(self):
        # line t*(2, 1) + (0, 1)
        a = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        # with -v
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(-2.0, -1.0))
        self.assertTrue(line2_qeq(a, b, fe))
        # with 2*v
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(4.0, 2.0))
        self.assertTrue(line2_qeq(a, b, fe))
        # at t=0 and t=1
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Point2(6.0, 4.0))
        self.assertTrue(line2_qeq(a, b, fe))
        # at t=-1 and t=2
        b = eu.Line2(eu.Point2(-2.0, 0.0), eu.Point2(4.0, 3.0))
        self.assertTrue(line2_qeq(a, b, fe))
        # with float, expect same direction but with norm == the float
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0), 7.0)
        self.assertTrue(line2_qeq(a, b, fe))
        self.assertTrue(abs(b.v.magnitude() - 7)<fe)
        # same as before but pass an int
        b = eu.Line2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0), 7)
        self.assertTrue(line2_qeq(a, b, fe))
        self.assertTrue(abs(b.v.magnitude() - 7)<fe)
        # with Line2, expect equal
        b = eu.Line2(a)
        self.assertTrue(line2_qeq(a, b, fe))

    def test_Ray2_basics(self):
        # ray t*(2, 1) + (0, 1)
        a = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        # with -v
        b = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(-2.0, -1.0))
        self.assertFalse(ray2_qeq(a, b, fe))
        # with 2*v
        b = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(4.0, 2.0))
        self.assertTrue(ray2_qeq(a, b, fe))
        # with float, expect same direction but with norm == abs(float)
        b = eu.Ray2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0), 7.0)
        self.assertTrue(ray2_qeq(a, b, fe))
        self.assertTrue(abs(b.v.magnitude() - 7)<fe)
        # with Ray2, expect equal
        b = eu.Ray2(a)
        self.assertTrue(ray2_qeq(a, b, fe))

    def test_LineSegment2_basics(self):
        # line t*(2, 1) + (0, 1)
        a = eu.LineSegment2(eu.Point2(0.0, 1.0), eu.Vector2(2.0, 1.0))
        # with LineSegment2, expect equal
        b = eu.LineSegment2(a)
        self.assertTrue(linesegment2_qeq(a, b, fe))

def circle_qec(c1, c2, qe):
    assert isinstance(c1, eu.Circle) and isinstance(c2, eu.Circle)
    return abs(c1.c - c2.c) + abs(c1.r - c2.r) < qe

class Test_Circle(unittest.TestCase):
    def test_circle_basics(self):
        a = eu.Circle(eu.Point2(1,2), 7.0)
        b = eu.Circle(eu.Point2(1,2), 7)
        self.assertTrue(circle_qec(a, b, fe))

class Test_Circle_intersect(unittest.TestCase):
    # here Circle was in fact considered a 'disk' aka 'Ball2'
    def test_LineSegment2(self):
        C = eu.Circle(eu.Point2(0, 0), 1.0)
        # segment outside
        self.assertEqual(None,
            C.intersect(eu.LineSegment2(eu.Point2(-3, 0), eu.Point2(-2, 0))))
        # segment inside
        ls = eu.LineSegment2(eu.Point2(-0.5, 0), eu.Point2(0.5, 0))
        self.assertTrue(linesegment2_qeq(ls, C.intersect(ls), fe))
        # cross one
        ls = eu.LineSegment2(eu.Point2(0.5, 0), eu.Point2(1.5, 0))
        expect = eu.LineSegment2(eu.Point2(0.5, 0), eu.Point2(1.0, 0))
        self.assertTrue(linesegment2_qeq(expect, C.intersect(ls), fe))
        # cross two
        ls = eu.LineSegment2(eu.Point2(-2, 0), eu.Point2(2.0, 0))
        expect = eu.LineSegment2(eu.Point2(-1, 0), eu.Point2(1.0, 0))
        self.assertTrue(linesegment2_qeq(expect, C.intersect(ls), fe))
        # tangent
        ls = eu.LineSegment2(eu.Point2(-1, 1), eu.Point2(1.0, 1))
        expect = eu.Point2(0, 1)
        self.assertTrue(abs(expect - C.intersect(ls)) < fe)

    def test_Ray2(self):
        C = eu.Circle(eu.Point2(0, 0), 1.0)
        # ray outside
        self.assertEqual(None,
            C.intersect(eu.Ray2(eu.Point2(2, 0), eu.Vector2(1, 0))))
        # cross one
        ls = eu.Ray2(eu.Point2(0.5, 0), eu.Vector2(1, 0))
        expect = eu.LineSegment2(eu.Point2(0.5, 0), eu.Point2(1.0, 0))
        self.assertTrue(linesegment2_qeq(expect, C.intersect(ls), fe))
        # cross two
        ls = eu.Ray2(eu.Point2(-2, 0), eu.Vector2(1, 0))
        expect = eu.LineSegment2(eu.Point2(-1, 0), eu.Point2(1.0, 0))
        self.assertTrue(linesegment2_qeq(expect, C.intersect(ls), fe))
        # tangent
        ls = eu.Ray2(eu.Point2(-1, 1), eu.Vector2(1.0, 0))
        expect = eu.Point2(0, 1)
        self.assertTrue(abs(expect - C.intersect(ls)) < fe)

    def test_Line2(self):
        C = eu.Circle(eu.Point2(0, 0), 1.0)
        # line outside
        self.assertEqual(None,
            C.intersect(eu.Line2(eu.Point2(0, 2), eu.Vector2(1, 0))))
        # cross two
        ls = eu.Line2(eu.Point2(-2, 0), eu.Vector2(1, 0))
        expect = eu.LineSegment2(eu.Point2(-1, 0), eu.Point2(1.0, 0))
        self.assertTrue(linesegment2_qeq(expect, C.intersect(ls), fe))
        # tangent
        ls = eu.Line2(eu.Point2(-1, 1), eu.Vector2(1.0, 0))
        expect = eu.Point2(0, 1)
        self.assertTrue(abs(expect - C.intersect(ls)) < fe)

class Test_Point3(unittest.TestCase):
    def test_swizzle_get(self):
        xyz = (1.0, 2.0, 3.0)
        v3 = eu.Point3(*xyz)
        self.assertEqual(v3.x, xyz[0])
        self.assertEqual(v3.y, xyz[1])
        self.assertEqual(v3.z, xyz[2])

        self.assertEqual(v3.xy, (xyz[0], xyz[1]))
        self.assertEqual(v3.xz, (xyz[0], xyz[2]))
        self.assertEqual(v3.yz, (xyz[1], xyz[2]))

        self.assertEqual(v3.yx, (xyz[1], xyz[0]))
        self.assertEqual(v3.zx, (xyz[2], xyz[0]))
        self.assertEqual(v3.zy, (xyz[2], xyz[1]))

        self.assertEqual(v3.xyz, xyz)
        self.assertEqual(v3.xzy, (xyz[0], xyz[2], xyz[1]) )
        self.assertEqual(v3.zyx, (xyz[2], xyz[1], xyz[0]) )
        self.assertEqual(v3.zxy, (xyz[2], xyz[0], xyz[1]) )
        self.assertEqual(v3.yxz, (xyz[1], xyz[0], xyz[2]) )
        self.assertEqual(v3.yzx, (xyz[1], xyz[2], xyz[0]) )

def point_nearest_0(L):
    assert isinstance(L, eu.Line3)
    t = - L.p.dot(L.v) / L.v.magnitude_squared()
    p = L.p + t * L.v
    return p

def test_point_nearest_0():
    # take p an unit vector, take the line that pass over p with direction
    # an orthogonal vector; expect p the nearest to 0
    L = eu.Line3(eu.Point3(1, 0, 0), eu.Vector3(0, 1, 0))
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    # with multiplied v, expect same result
    L = eu.Line3(eu.Point3(1, 0, 0), eu.Vector3(0, 7, 0))
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    # with -v, expect same result
    L = eu.Line3(eu.Point3(1, 0, 0), eu.Vector3(0, -1, 0))
    # moving p along the line, expect same result
    L = eu.Line3(eu.Point3(1, 11, 0), eu.Vector3(0, 7, 0))
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    ## similar with the other ortho vector
    L = eu.Line3(eu.Point3(1, 0, 0), eu.Vector3(0, 0, 1))
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    # with multiplied v
    L = eu.Line3(eu.Point3(1, 0, 0), eu.Vector3(0, 0, 7))
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    # moving p along the line
    L = eu.Line3(eu.Point3(1, 0, 11), eu.Vector3(0, 0, 7))
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    ## similar with a combo ortho vector
    w = eu.Vector3(0, 1, 1)
    L = eu.Line3(eu.Point3(1, 0, 0), w)
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    # with multiplied v
    L = eu.Line3(eu.Point3(1, 0, 0), 7 * w)
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe
    # moving p along the line
    L = eu.Line3(eu.Point3(1, 0, 0) + 11*w, w)
    assert abs(point_nearest_0(L) - eu.Point3(1, 0, 0)) < fe

# helper to assert Line3 equals
def line3_normal_rep(L):
    "p the point in line nearest to 0, v with |v|=1 and 1st component nonzero >0"
    assert isinstance(L, eu.Line3)
    p = point_nearest_0(L)
    v = L.v.normalized()
    if v.x < 0:
        v = -v
    elif v.x == 0:
        if v.y < 0:
            v = -v
        elif v.y == 0:
            if v.z < 0:
                v = -v
    return eu.Line3(p, v)

def line3_qeq(line1, line2, qe):
    "Line2 quasi equal"
    L1 = line3_normal_rep(line1)
    L2 = line3_normal_rep(line2)
    return abs(L1.p - L2.p) + abs(L1.v - L2.v) < qe

def ray3_qeq(ray1, ray2, qe):
    assert isinstance(ray1, eu.Ray3) and isinstance(ray2, eu.Ray3)
    return abs(ray1.p - ray2.p) + abs(ray1.v.normalized() - ray2.v.normalized()) < qe

def linesegment3_qeq(ls1, ls2, qe):
    "LineSegment3 quasi equal, unoriented"
    assert isinstance(ls1, eu.LineSegment3) and isinstance(ls2, eu.LineSegment3)
    if abs(ls1.p - ls2.p) + abs(ls1.v - ls2.v) < qe:
        return  True
    q = ls1.p + ls1.v
    w = - ls1.v
    return abs(q - ls2.p) + abs(w - ls2.v) < qe

class Test_Line3_family(unittest.TestCase):
    def test_basic_sanity__line3_qeq(self):
        # line t*(2, 1, 7) + (0, 1, 0)
        a = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        # same p, same v -> True
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        self.assertTrue(line3_qeq(a, b, fe))
        # same v, different p -> False
        b = eu.Line3(eu.Point3(0.0, 0.9, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        self.assertFalse(line3_qeq(a, b, fe))
        # non-parallel v, same p -> False
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.1, 7.0))
        self.assertFalse(line3_qeq(a, b, fe))

    def test_Line3_basics(self):
        # line t*(2, 1, 7) + (0, 1, 0)
        a = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        # with -v
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(-2.0, -1.0, -7.0))
        self.assertTrue(line3_qeq(a, b, fe))
        # with 2*v
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(4.0, 2.0, 14.0))
        self.assertTrue(line3_qeq(a, b, fe))
        # at t=0 and t=1
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Point3(2.0, 2.0, 7.0))
        self.assertTrue(line3_qeq(a, b, fe))
        # at t=-1 and t=2
        b = eu.Line3(eu.Point3(-2.0, 0.0, -7.0), eu.Point3(4.0, 3.0, 14.0))
        self.assertTrue(line3_qeq(a, b, fe))
        # with float, expect same direction but with norm == the float
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0), 7.0)
        self.assertTrue(line3_qeq(a, b, fe))
        self.assertTrue(abs(b.v.magnitude() - 7)<fe)
        # same as before but pass an int
        b = eu.Line3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0), 7)
        self.assertTrue(line3_qeq(a, b, fe))
        self.assertTrue(abs(b.v.magnitude() - 7)<fe)
        # with Line3, expect equal
        b = eu.Line3(a)
        self.assertTrue(line3_qeq(a, b, fe))

    def test_basic_sanity__ray3_qeq(self):
        # line t*(2, 1, 7) + (0, 1, 0)
        a = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        # same p, same v -> True
        b = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        self.assertTrue(ray3_qeq(a, b, fe))
        # same v, different p -> False
        b = eu.Ray3(eu.Point3(0.0, 0.9, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        self.assertFalse(ray3_qeq(a, b, fe))
        # non-parallel v, same p -> False
        b = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.1, 7.0))
        self.assertFalse(ray3_qeq(a, b, fe))

    def test_Ray3_basics(self):
        # line t*(2, 1, 7) + (0, 1, 0)
        a = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0))
        # with -v
        b = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(-2.0, -1.0, -7.0))
        self.assertFalse(ray3_qeq(a, b, fe))
        # with 2*v
        b = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(4.0, 2.0, 14.0))
        self.assertTrue(ray3_qeq(a, b, fe))
        # with float, expect same direction but with norm == abs(float)
        b = eu.Ray3(eu.Point3(0.0, 1.0, 0.0), eu.Vector3(2.0, 1.0, 7.0), 7.0)
        self.assertTrue(ray3_qeq(a, b, fe))
        self.assertTrue(abs(b.v.magnitude() - 7)<fe)
        # with Ray3, expect equal
        b = eu.Ray3(a)
        self.assertTrue(ray3_qeq(a, b, fe))

    def test_basic_sanity__linesegment3_qeq(self):
        # with itself
        a = eu.Point3(1, 2, 7); b = eu.Point3(5, 11, 19)
        r = eu.LineSegment3(a, b)
        self.assertTrue(linesegment3_qeq(r, r, fe))
        # with reversed
        s = eu.LineSegment3(b, a)
        self.assertTrue(linesegment3_qeq(r, s, fe))
        # with different
        b = eu.Point3(5, 11, 19.1)
        s = eu.LineSegment3(a, b)
        self.assertFalse(linesegment3_qeq(r, s, fe))

    def test_LineSegment3_basics(self):
        # line t*(2, 1) + (0, 1)
        a = eu.LineSegment3(eu.Point3(0.0, 1.0, 11.0), eu.Vector3(2.0, 1.0, 7.0))
        # with LineSegment3, expect equal
        b = eu.LineSegment3(a)
        self.assertTrue(linesegment3_qeq(a, b, fe))

if __name__ == '__main__':
    unittest.main()
