import socket
import subprocess
import os

class VirtualHand(object):
    """VRE virtual hand interface in Python.

    Parameters
    ----------
    app_path : str
        Path of the Virtual Reality application. If provided, the application
        will be executed. If not provided, it is assumed that the applicaiton
        is already running.
    """
    def __init__(self, app_path=None):
        self.app_path = app_path
        self._app_running = True if self.app_path is None else False

        self._init()

    def _init(self):
        """Run VRE application and initalize the socket connection."""
        if not self._app_running:
            subprocess.Popen([self.app_path])

        # Server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 23068))
        self.server.listen(5)

        # Client socket
        self.client, self.client_addr = self.server.accept()

    def init_arm(self):
        self.client._send_command('c111')

    def init_leg(self):
        self.client._send_command('c211')

    def switch_side(self):
        self.client._send_command('c511')

    def switch_position(self):
        self.client._send_command('c611')

    def switch_camera(self, camera):
        """Sets the camera.

        Parameters
        ---------
        camera : int (0 <= camera <= 4)
            Camera number.
        """
        self.client._send_command('c4' + str(camera) + '1')

    def move_limb(self, limb, dof, direction, speed, fraction):
        """Move the specifidied DOF.

        Parameters
        ----------

        """
        self.client._send_command(
            str(limb) + str(dof) + str(direction) + str(speed) + str(fraction)
        )

    def _format_message(self, message):
        """Format command.

        Parameters
        ----------
        command : str
            Command in string format.
        """
        msg = []
        for i in message:
            try:
                msg.append(chr(int(i)))
            except ValueError:
                msg.append(i)

        msg = ''.join(msg).encode('utf-8')
        return msg

    def _send_command(self, message):
        message = self._format_message(message)
        self.client.send(message)
        recv_msg = self.client.recv(1)
        return recv_msg

    def stop(self):
        self.client.close()
        self.server.close()

    def __del__(self):
        try:
            self.stop()
        except BaseException:
            pass
