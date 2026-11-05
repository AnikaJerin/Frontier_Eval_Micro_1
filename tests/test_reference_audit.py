import json,math,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'data'
def ref(name):return json.loads((R/(name+'.json')).read_text())['reference']
class IndependentArithmetic(unittest.TestCase):
 def test_synop_sign_and_pressure(self):
  r=ref('synop_cold');self.assertEqual(r,{'air_temperature_c':-25/10,'dewpoint_c':-48/10,'msl_pressure_hpa':9987/10})
  r=ref('synop_trend');self.assertAlmostEqual(r['current_msl_pressure_hpa'],9987/10);self.assertAlmostEqual(r['msl_pressure_three_hours_ago_hpa'],9987/10-18/10);self.assertAlmostEqual(r['temperature_dewpoint_spread_c'],-25/10-(-48/10))
 def test_conditional_cross_code_and_absence(self):
  r=ref('cross_code');self.assertEqual(math.floor(r['synop_msl_pressure_hpa']),r['metar_qnh_hpa']);self.assertIsNone(r['metar_ceiling_ft_agl']);self.assertEqual((r['synop_temperature_c'],r['synop_dewpoint_c']),(-.8,-1.2))
  r=ref('T13');self.assertIsNone(r['c_dew_c']);self.assertIsNone(r['c_msl_hpa']);self.assertIsNone(r['c_spread_c']);self.assertAlmostEqual(r['b_minus_a_msl_hpa'],1003.2-998.7)
 def test_taf_timeline(self):
  r=ref('taf_four_times');self.assertEqual([r[k] for k in ('p1559','temp1559','p1600','temp1600','p1900','temp1900','p0000','temp0000')],[6000,800,None,None,None,1200,1200,None])
