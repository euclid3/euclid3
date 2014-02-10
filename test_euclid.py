from __future__ import division, print_function, unicode_literals

import euclid as eu
import unittest

class Test_Vector2(unittest.TestCase):
    def test_instantiate(self):
        xy = (1.0, 2.0)
        v2 = eu.Vector2(*xy)
        self.assertEquals(repr(v2), "Vector2(%.2f, %.2f)" % xy)

    def test_instantiate_default(self):
        v2 = eu.Vector2()
        self.assertEquals(repr(v2), "Vector2(%.2f, %.2f)" % (0, 0))

    def test_copy(self):
        xy = (1.0, 2.0)
        v2 = eu.Vector2(*xy)

        copy = v2.__copy__()
        self.assertEquals(repr(v2), repr(copy))
        self.assertFalse(copy is v2)

    def test_eq_v2(self):
        xy = (1.0, 2.0)
        self.assertTrue(eu.Vector2(*xy), eu.Vector2(*xy))

        other = (1.0, 3.0)
        self.assertTrue( eu.Vector2(*xy) != eu.Vector2(*other))

    def test_eq_tuple(self):
        xy = (1.0, 2.0)
        self.assertEquals(eu.Vector2(*xy), xy)

        other = (1.0, 2.0, 3.0)
        self.assertRaises( AssertionError,
                           lambda a, b: a == b, eu.Vector2(*xy), other)

        other = 1.0
        self.assertRaises( AssertionError,
                           lambda a, b: a == b, eu.Vector2(*xy), other)

    def test_len(self):
        xy = (1.0, 2.0)
        self.assertEquals(len(eu.Vector2(*xy)), 2)
        
    def test_index_access__get(self):
        xy = (1.0, 2.0)
        v2 = eu.Vector2(*xy)
        self.assertEquals( v2[0], xy[0])
        self.assertEquals(v2[1], xy[1])
        self.assertRaises(IndexError,
                          lambda a: v2[a], 2)

    def test_index_access__set(self):
        xy = (1.0, 2.0)
        v2 = eu.Vector2(*xy)
        v2[0] = 7.0
        self.assertEquals(repr(v2), "Vector2(%.2f, %.2f)" % (7.0, 2.0))
        v2[1] = 8.0
        self.assertEquals(repr(v2), "Vector2(%.2f, %.2f)" % (7.0, 8.0))
        def f():
            v2[2] = 9.0 
        self.assertRaises(IndexError, f)

    def test_iter(self):
        xy = [1.0, 2.0]
        v2 = eu.Vector2(*xy)
        sequence = [e for e in v2]
        self.assertEquals(sequence, xy)
        
    def test_swizzle_get(self):
        xy = (1.0, 2.0)
        v2 = eu.Vector2(*xy)
        self.assertEquals(v2.x, xy[0])
        self.assertEquals(v2.y, xy[1])
        self.assertEquals(v2.xy, xy)

        exception = None
        try:
            v2.z == 11.0
        except Exception as a:
            exception = a
        assert isinstance(exception, AttributeError)
        
    def test_vector2_rsub(self):
        a = (3.0, 7.0)
        b = (1.0, 2.0)
        va = eu.Vector2(*a)
        vb = eu.Vector2(*b)
        self.assertEquals(va-vb, eu.Vector2(2.0, 5.0))
        self.assertEquals(va-b, eu.Vector2(2.0, 5.0))
        self.assertEquals(a-vb, eu.Vector2(2.0, 5.0))
        

class Test_Vector3(unittest.TestCase):

    def test_vector3_rsub(self):
        a = (3.0, 7.0, 9.0)
        b = (1.0, 2.0, 3.0)
        va = eu.Vector3(*a)
        vb = eu.Vector3(*b)
        self.assertEquals(va-vb, eu.Vector3(2.0, 5.0, 6.0))
        self.assertEquals(va-b, eu.Vector3(2.0, 5.0, 6.0))
        self.assertEquals(a-vb, eu.Vector3(2.0, 5.0, 6.0))
        
    
if __name__ == '__main__':
    unittest.main()
