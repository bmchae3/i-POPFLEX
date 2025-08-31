# import library
from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "i-POSFLEX_pooling_etube",
    "author": "BMC <bmchae3@postech.ac.kr>",
    "description": "Automatic preparation of translational machinery_Trial 1",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

# protocol run function_Trial 1
def run(protocol: protocol_api.ProtocolContext):
    # load tip rack  
    tiprack2 = protocol.load_labware(
        load_name="opentrons_96_tiprack_300ul", location=4
    )
        
    # attach pipette to left mount
    p300 = protocol.load_instrument(
        instrument_name="p300_single_gen2",
        mount="left",
        tip_racks=[tiprack2]
    )
    
    # load conical tube rack in deck slot 5
    rack = protocol.load_labware(
        load_name="opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", location=7        #conical tube rack
    )
       
    # Load temperature module in deck slot 10
    reaction_plate1 = protocol.load_labware(
        load_name="axygen_24_aluminumblock_1500ul", location=5
    )
    reaction_plate2 = protocol.load_labware(
        load_name="axygen_24_aluminumblock_1500ul", location=6
    )
    # Pooling   
    reactions = (
    [reaction_plate1[f"{row}{col}"] for row in ["A","B","C","D"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["A"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["B"] for col in [1,2,3]]
    )
           
    p300.transfer(
    45,                                                                        # Volume(µL)
    reactions,                                                                 # A1-12 of dna_plate
    rack["A2"],                                                                # A1-12 of temp_combo
    mix_before=(2, 40),                                                        # Pipetting
    new_tip='once'                                                           # Different pipet tip  
    )