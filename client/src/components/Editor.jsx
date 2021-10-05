import React, {useContext} from 'react'
import AceEditor from "react-ace";
import codeContext from "../context/Code/CodeContext";

const Editor = () => {
  const CodeContext = useContext(codeContext);

  const onChange = (newCode) => {
    CodeContext.setCode(newCode);
  };

  return (
    <>
      <AceEditor
        style={{'borderRadius': '1%', 'width': '100%'}}
        placeholder="Your code goes here"
        mode="javascript"
        theme="monokai"
        name="mainEditor"
        onChange={onChange}
        fontSize={16}
        showPrintMargin={true}
        showGutter={true}
        highlightActiveLine={true}
        value={CodeContext.code}
        editorProps={{
          $blockScrolling: true
        }}
        enableBasicAutocompletion={true}
        enableLiveAutocompletion={true}
        enableSnippets={true}
      />
    </>
  )
};

export default Editor;
