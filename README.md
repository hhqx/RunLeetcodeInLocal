# Run LeetCode in Local Python IDE

**This is a package help you to run in local python IDE.**



## Installation

- pip install
```shell
pip install git+https://github.com/hhqx/RunLeetcodeInLocal.git
```



## Edit local template

### template in PyCharm

```

question_content = ${question.content}

from typing import *
from PythonLeetcodeRunner import *

${question.code} 


if __name__ == "__main__":
    TestObj = StartTest(question_content, Solution)
    TestObj.run_test()

```

### template in VS-Code

- file path (windows)

  ```
  C:\Users\USER_NAME\.vscode\extensions\leetcode.vscode-leetcode-0.18.1\node_modules\vsc-leetcode-cli\templates\detailed.tpl
  ```

- content

  ```
  ${comment.start}
  ${comment.line} @lc app=${app} id=${fid} lang=${lang}
  ${comment.line}
  ${comment.line} [${fid}] ${name}
  ${comment.line}
  ${comment.line} ${link}
  ${comment.line}
  ${comment.line} ${category}
  ${comment.line} ${level} (${percent}%)
  ${comment.line} Likes:    ${likes}
  ${comment.line} Dislikes: ${dislikes}
  ${comment.line} Total Accepted:    ${totalAC}
  ${comment.line} Total Submissions: ${totalSubmit}
  ${comment.line} Testcase Example:  ${testcase}
  ${comment.line}
  
  question_content="""{{ desc.forEach(function(x) { }}${x}
  {{}) }}"""
  
  from typing import *
  from PythonLeetcodeRunner import *
  
  ${comment.singleLine} @lc code=start
  ${code}
          return
  ${comment.singleLine} @lc code=end
  
  
  if __name__ == "__main__":
      TestObj = StartTest(question_content, Solution)
      TestObj.run_test()
  
  ```

  



