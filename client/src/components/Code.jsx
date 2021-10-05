import React, {useContext, useState, useRef, useEffect} from 'react';
import codeContext from '../context/Code/CodeContext';
import {Button, Layout, Row, Col, Typography, Modal, Table, Form, Input, Spin, message, Tabs} from "antd";

import Emulator from "./Emulator";
import Editor from "./Editor";

const {ipcRenderer} = window.require("electron");

const {Header, Footer, Content} = Layout;
const {Title} = Typography;
const FormItem = Form.Item;
const TabPane = Tabs.TabPane
const { TextArea } = Input;

const Code = () => {
  return (
    <>
      <CodeIn/>
      <div style={{'marginTop': 20, 'marginBottom': 20}}>
        <ModalCodesMain/>
        <ModalFormMain/>
      </div>
    </>
  )
}

const ModalCodesMain = () => {
  const [modalCodesShow, setModalCodesShow] = useState(false);

  const ModalCodes = () => {
    const CodeContext = useContext(codeContext);
    const [filter, setFilter] = useState("examples")

    useEffect(() => {
      CodeContext.getCodes(filter)
    }, [filter])

    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      render: (text, record) => (
        <span>
      <a onClick={() => {
        setModalCodesShow(false)
        CodeContext.setCode(record.code)
      }}>{record.name}</a>
    </span>
      ),
    }, {
      title: 'Author',
      dataIndex: 'author',
    }, {
      title: 'Description',
      dataIndex: 'description',
    }]

    const ModalTable = () => {
      return (
        <Table columns={columns} dataSource={CodeContext.codes} rowKey='pk'/>
      )
    }

    return (
      <>
        <Tabs
          defaultActiveKey="examples"
          centered
          onChange={(key) => {
            setFilter(key)
            CodeContext.getCodes(filter)
          }}
        >
          <TabPane
            tab={
              <span style={{width: 200}}>
                Examples
               </span>
            }
            key="examples">
          </TabPane>
          <TabPane
            tab={
              <span style={{width: 200}}>
                Approved
               </span>
            }
            key="approved">
          </TabPane>
          <TabPane
            tab={
              <span>
                All
               </span>
            }
            key="all">
          </TabPane>
        </Tabs>
        <ModalTable/>
      </>
    )
  }

  return (
    <>
      <Button style={{'marginLeft': 30}} onClick={() => {
        setModalCodesShow(true)
      }}>Codes</Button>

      <Modal
        title="Codes"
        style={{}}
        width={1000}
        visible={modalCodesShow}
        onOk={() => setModalCodesShow(false)}
        onCancel={() => setModalCodesShow(false)}
        footer={[]}
      >
        <ModalCodes/>
      </Modal>

    </>
  )
}

const ModalFormMain = () => {
  const [modalFormShow, setModalFormShow] = useState(false);

  const ModalForm = () => {
    const form = useRef(null);
    const [sending, setSending] = useState(false)
    const CodeContext = useContext(codeContext);

    return (
      <Modal
        title="Submit"
        style={{}}
        width={500}
        visible={modalFormShow}
        onOk={(f) => {
          form.current.submit()
        }}
        onCancel={() => setModalFormShow(false)}
      >
        <Spin spinning={sending}>
          <Form
            name="normal_login"
            ref={form}
            onFinish={(e) => {
              console.log(e)
              setSending(true)
              CodeContext.submitCode(e)
                .then(() => {
                  setSending(false)
                  setModalFormShow(false)
                  message.success('Successfully sent animation');
                })
                .catch(() => {
                  message.error('Sending animation failed');
                  setSending(false)
                })
            }}
          >
            <FormItem
              label="Name"
              name="name"
              rules={[{required: true, message: 'Please input a name!'}]}
            >
              <Input/>
            </FormItem>
            <FormItem
              label="Author"
              name="author"
              rules={[{required: true, message: 'Please input a author name!'}]}
            >
              <Input/>
            </FormItem>
            <FormItem
              label="Description"
              name="description"
            >
              <TextArea/>
            </FormItem>
          </Form>
        </Spin>
      </Modal>
    )
  }

  return (
    <>
      <Button style={{'marginLeft': 15}} onClick={() => {
        setModalFormShow(true)
      }}>Submit</Button>
      <ModalForm/>
    </>
  )
}

const CodeIn = () => {
  const CodeContext = useContext(codeContext);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    ipcRenderer.on('stop', (event) => {
      setRunning(false);
    })

    ipcRenderer.on('error', (event, arg) => {
      message.error(arg);
      setRunning(false);
    })

    ipcRenderer.on('log', (event, arg) => {
      message.info(arg);
    })
  }, []);

  return (
    <>
      <Layout style={{'marginTop': 20, 'marginLeft': 30}}>
        <Header style={{'backgroundColor': '#fff'}}>
          <Row style={{'marginLeft': 50}}>
            <Col>
              <Title>Emulator</Title>
            </Col>
            <Col style={{'marginLeft': 50}}>
              {!CodeContext.liveMode && !running &&
              <Button onClick={() => {
                ipcRenderer.send('code', CodeContext.code);
                setRunning(true);
              }}>Run</Button>
              }
              {
                running &&
                <Button onClick={() => {
                  ipcRenderer.send('stop');
                }}>Stop</Button>
              }

              {!running && !CodeContext.liveMode &&
              <Button style={{'marginLeft': 15}} onClick={() => {
                CodeContext.setLiveMode(true)}
              }>
                Live Mode
              </Button>
              }
              {CodeContext.liveMode &&
              <Button style={{'marginLeft': 15}} onClick={() => {
                CodeContext.setLiveMode(false)
              }}>Exit live mode</Button>
              }

            </Col>
          </Row>
        </Header>
        <Content style={{'backgroundColor': 'white'}}>
          <Row>
            <Col xs={24} xl={12}>
              <Emulator/>
            </Col>
            <Col xs={24} xl={12}>
              <Editor/>
            </Col>
          </Row>
        </Content>
      </Layout>
    </>
  )

};

export default Code;
