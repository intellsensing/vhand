import socket
import subprocess


class VirtualHand(object):
    """VRE virtual hand interface in Python.

    Parameters
    ----------
    app_path : str
        Path of the Virtual Reality application. If provided, the application
        will be executed. If not provided, it is assumed that the applicaiton
        is already running. If not provided and the application is not running,
        the program will crash.
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
        """Initialize an arm model (right arm)."""
        self._send_command('c111')

    def init_leg(self):
        """Initialize an leg model (right leg)."""
        self._send_command('c211')

    def switch_side(self):
        """Switch between right and left limb."""
        self._send_command('c511')

    def switch_position(self):
        """Switch between above elbow/knee and beneath elbow/knee."""
        self._send_command('c611')

    def switch_camera(self, camera):
        """Set which camera to look through.

        Parameters
        ---------
        camera : int (0 <= camera <= 4)
            Camera number.
        """
        self._send_command('c4' + str(camera) + '1')

    def move_limb(self, dof, direction, distance_n, distance_d=1, tac=False):
        """Move the specified DOF.

        The distance is represented using a fraction (nominator and
        denominator).

        Parameters
        ----------
        dof : int
            Degree-of-freedom

        direction : int (0 or 1)
            Direction to move. 0 indicates flexion and 1 extension.

        distance_n : int
            Distance to move in given direction (nominator).

        distance_d : int (default 1)
            Distance to move in given direction (denominator).

        tac : bool (default False)
            If True, move the TAC limb.

        Notes
        -----
        The support DOFs are given in the following table:

        DoF	Hand movement           Leg/Foot movement
        1	Pinky/Little - Pitch    Little Ext/Flex
        2	Ring Finger - Pitch     Ring Toe Extend/Flex
        3	Middle Finger- Pitch	Middle Toe Ext/Flex
        4	Index Finger - Pitch	Index Toe Ext/Flex
        5	Thumb - Pitch	        Big Toe Ext/Flex
        6	Thumb - Yaw           	Ankle Plantarflexion/Dorsiflexion
        7	Palm - Pitch          	Ankle Inversion/Eversion
        8	Palm - Roll           	Extend/Flex Knee
        9	Open/Close Hand       	Tibial Rotation In/Out
        10	Point                	Femoral Rotation In/Out
        11	Agree                	Toes Curl/Stretch
        """
        limb = 2 if tac else 1
        self._send_command(
            str(limb) + str(dof) + str(direction) + str(distance_n) + \
            str(distance_d)
        )

    def activate_tac(self):
        """Switch TAC test on."""
        self._send_command('c2111')

    def deactivate_tac(self):
        """Switch TAC test on."""
        self._send_command('c2011')

    def reset_position(self, tac=False):
        """Reset position.

        Parameters
        ----------
        tac : bool (default False)
            If True, reset the position of the TAC limb.
        """
        if tac:
            self._send_command('rt00')
        else:
            self._send_command('r000')


    def _format_message(self, message):
        """Format command.

        Parameters
        ----------
        message : str
            Message in string format.
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
        """Send command to client socket."""
        message = self._format_message(message)
        self.client.send(message)
        recv_msg = self.client.recv(1)
        return recv_msg

    def stop(self):
        """Stop the simulation and exit application."""
        self.client.close()
        self.server.close()

    def __del__(self):
        try:
            self.stop()
        except BaseException:
            pass
