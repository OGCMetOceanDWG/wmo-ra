
import sys
from osgeo import ogr

REGION_IDS = {
    1: ['I', 'Africa'],
    2: ['II', 'Asia'],
    3: ['III', 'South America'],
    4: ['IV', 'North America, Central America, Caribbean'],
    5: ['V', 'South-West Pacific'],
    6: ['VI', 'Europe'],
}


def is_valid(data):
    """test if dataset is valid"""
    dataset = ogr.Open(data)
    layer = dataset.GetLayer(0)
    geomtype = layer.GetGeomType()
    if geomtype != 6:
        print 'ERROR: Invalid Layer Geometry type: %d' % geomtype
        return False
    feature_count = layer.GetFeatureCount()
    if feature_count != 6:
        print 'ERROR: Invalid Feature Count: %d' % feature_count
    for feature in layer:
        if (feature.GetGeometryRef() is None or
           not feature.GetGeometryRef().IsValid()):
            print 'ERROR: Invalid Geomtry'
            return False
        wmo_ra = feature.GetField('WMO_RA')
        roman_num = feature.GetField('roman_num')
        region = feature.GetField('region')
        if wmo_ra not in REGION_IDS:
            print 'Invalid WMO RA value: %d' % wmo_ra
            return False
        if REGION_IDS[wmo_ra][0] != roman_num:
            print 'WMO RA/roman numeral mismatch: %s/%s' % \
                (REGION_IDS[wmo_ra][0], roman_num)
            return False
        if REGION_IDS[wmo_ra][1] != region:
            print 'Invalid reigon: %s' % region
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s <data>' % sys.argv[0]
        sys.exit(1)

    if not is_valid(sys.argv[1]):
        print 'Invalid'
        sys.exit(2)

    print 'Valid'
