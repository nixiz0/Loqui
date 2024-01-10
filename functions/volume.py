from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
        
        
def set_volume(vol):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        interface = session._ctl.QueryInterface(ISimpleAudioVolume)
        # set the volume (0.0 to 1.0)
        interface.SetMasterVolume(vol, None)
        
def change_volume(delta):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        interface = session._ctl.QueryInterface(ISimpleAudioVolume)
        # Get the actual volume
        current_volume = interface.GetMasterVolume()
        # Calcul the new volume
        new_volume = max(0.0, min(1.0, current_volume + delta))
        # Set the volume
        interface.SetMasterVolume(new_volume, None)