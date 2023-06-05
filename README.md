整体框架分层：
API层：负责封装各个接口，提供可调用的接口方法。将api层分成两个部分：
api_base：负责封装公共的请求参数、请求头等信息。
具体api层：负责封装具体的接口请求，通过api_base层提供的方法，发送请求。

service层：负责封装多个api的调用流程，提供可调用的流程方法。将service层分成两个部分：
service_base层：负责封装公共的流程处理方法，如登录、退出等。
具体service层：负责封装具体的业务流程，通过调用多个api层提供的方法，完成业务流程。

testcase层：负责编排用例，调用service层的关键字，完成用例执行，测试数据与用例分离
分为：
testcase
testdata

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
