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
        self.assertEqual(va-vb, eu.Vector3(2.0, 5.0, 6.0))
        
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
    
if __name__ == '__main__':
    unittest.main()
