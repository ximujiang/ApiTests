
## validate 可以支持的校验方式

| comparator               | 缩写                                   | 功能                                      |
|:-------------------------|--------------------------------------|-----------------------------------------|
| equal                    | 	“eq”, “equals”, “equal”             | 	相等                                     |
| less_than                | 	“lt”, “less_than”	                  | 小于                                      |
| less_or_equals           | 	“le”, “less_or_equals”	             | 小于或等于                                   |
| greater_than             | 	“gt”, “greater_than”	               | 大于                                      |
| greater_or_equals        | 	“ge”, “greater_or_equals”	          | 大于或等于                                   |
| not_equal                | 	“ne”, “not_equal”	                  | 不等于                                     |
| string_equals            | 	“str_eq”, “string_equals”	          | 转字符串相等                                  |
| length_equal             | 	“len_eq”, “length_equal”	           | 长度相等                                    |
| length_greater_than      | 	“len_gt”,“length_greater_than”      | 长度大于                                    |
| length_greater_or_equals | 	“len_ge”,“length_greater_or_equals” | 长度大于或等于                                 |
| length_less_than         | 	“len_lt”, “length_less_than”	       | 长度小于                                    |
| length_less_or_equals    | 	“len_le”, “length_less_or_equals”   | 	 长度小于或等于                               |
| contains                 | 		                                   | check_value 包含 expect_value             |
| contained_by             | 		                                   | expect_value 包含check_value              |
| type_match               | 		                                   | type类型匹配                                |
| regex_match              | 		                                   | 正则匹配re.match(expect_value, check_value) |
| startswith               | 		                                   | 字符串以xx开头                                |
| endswith                 | 		                                   | 字符串以xx结尾                                |
