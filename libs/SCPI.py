# -*- encoding:UTF-8 -*-
import pyvisa
import ConsolePrint
sys_error = '*ESR?'
sys_version = 'SYST:VERS?'
sys_remote = 'SYST:REM'
sys_local = 'SYST:LOC'
sys_rwlock = 'SYST:RWL'
sys_beeper = 'SYST:BEEP'
output_on = 'OUTP 1'
output_off = 'OUTP 0'
voltage_value_set = 'VOLT %s'
voltage_query = 'VOLT?'
ampere_value_set = 'CURR %s'
ampere_query = 'CURR?'


def get_serial_source():
    rm = pyvisa.ResourceManager()
    return rm.list_resources()



def param_to_property(*props, **kwprops):
    if props and kwprops:
        raise SyntaxError("Can not set both props and kwprops at the same time.")

    class Wrapper(object):
        def __init__(self, func):
            self.func = func
            self.kwargs, self.args = {}, []

        def __getattr__(self, attr):
            if kwprops:
                for prop_name, prop_values in kwprops.items():
                    if attr in prop_values and prop_name not in self.kwargs:
                        self.kwargs[prop_name] = attr
                        return self
            elif attr in props:
                self.args.append(attr)
                return self
            raise AttributeError("%s parameter is duplicated or not allowed!" % attr)

        def __call__(self, *args, **kwargs):
            if kwprops:
                kwargs.update(self.kwargs)
                self.kwargs = {}
                return self.func(*args, **kwargs)
            else:
                new_args, self.args = self.args + list(args), []
                return self.func(*new_args, **kwargs)

    return Wrapper


class SerialInstrument(object):
    def __init__(self, port):
        self.__port = port
        self.__session = None
        self.__init_session()

    @property
    def power(self):
        @param_to_property(action=["on", "off"])
        def _power(action='off'):
            if action == "on":
                return self._send_command(cmd=output_on)
            else:
                return self._send_command(cmd=output_off)

        return _power

    @property
    def voltage(self):
        @param_to_property(action=["set", "query"])
        def _voltage(action='set', val='5'):
            if action == 'set':
                return self._send_command(voltage_value_set % val)
            elif action == 'query':
                return self._send_command(voltage_query)

        return _voltage

    @property
    def ampere(self):
        @param_to_property(action=["set", "query"])
        def _ampere(action='set', val='2'):
            if action == 'set':
                return self._send_command(ampere_value_set % val)
            elif action == 'query':
                return self._send_command(ampere_query)

        return _ampere

    @property
    def system(self):
        @param_to_property(action=["remote", "local", "version", "error", "beeper", "rwlock"])
        def _system(action='version'):
            if action == "remote":
                return self._send_command(cmd=sys_remote)
            elif action == "local":
                return self._send_command(cmd=sys_local)
            elif action == "version":
                return self._send_command(cmd=sys_version)
            elif action == "error":
                return self._send_command(cmd=sys_error)
            elif action == "beeper":
                return self._send_command(cmd=sys_beeper)
            elif action == "rwlock":
                return self._send_command(cmd=sys_rwlock)

        return _system

    def __convert_port(self, port):
        port = port.replace('COM', '')
        port = 'ASRL%s::INSTR' % port
        return port

    def __init_session(self):
        try:
            rm = pyvisa.ResourceManager()
            self.__session = rm.open_resource(self.__port)
            self.__session.timeout = 1000
        except pyvisa.errors.VisaIOError:
            self.__session = None
            ConsolePrint.error('SCPI|Initialization serial instrument failure')

    def _send_command(self, cmd):
        if self.__session is None:
            return False, 'Session has not been established'
        if cmd.endswith('?'):
            ConsolePrint.debug("SCPI|Query  :%s" % cmd)
            exec_result = self.__query(cmd)

        else:
            ConsolePrint.debug("SCPI|Write  :%s" % cmd)
            exec_result = self.__write(cmd)
        error_msg = self.__query(sys_error)
        ConsolePrint.debug("SCPI|Result :%s" % str(exec_result))
        if error_msg == u'0':
            return True, exec_result
        else:
            ConsolePrint.debug("SCPI|ErrMsg :%s" % str(error_msg))
            return False, error_msg

    def __query(self, cmd):
        try:
            return self.__session.query(cmd).strip('\r\n')
        except pyvisa.errors.VisaIOError:
            return 'ERROR'

    def __write(self, cmd):
        return self.__session.write(cmd)


if __name__ == '__main__':
    import time
    print 'd'
    SI = SerialInstrument('USB0::0x0699::0x0408::C013076::INSTR')
    #
    # print SI.voltage.query()
    #
    # print SI.ampere.query()
    # for x in range(1000):
    #     print SI._send_command('MEASure:CURRent?')
    # time.sleep(10)
    # print SI._send_command('FETCh:CURRent?')
    # print SI._query(sys_version)
    # print SI._write(sys_remote)
    #
    # print SI._write(ampere_set)
    # print SI._query(sys_error)
    # print SI._query(sys_error)
    # print SI.write('SYST:BEEP')
    print 's'
    SI._send_command('MEASUrement:IMMed:TYPe MEAN')
    for x in range(100):
        print x
        time.sleep(1)
        SI._send_command('MEASUrement:IMMed:SOUrce CH4')
        print SI._send_command('MEASUrement:IMMed:VALue?')
        SI._send_command('MEASUrement:IMMed:SOUrce CH1')
        print SI._send_command('MEASUrement:IMMed:VALue?')

    # print SI._write('OUTPut 1')
#