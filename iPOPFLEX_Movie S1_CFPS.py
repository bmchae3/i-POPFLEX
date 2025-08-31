# import library
from opentrons import protocol_api

# metadata
metadata = {
    "protocolName": "i-POPFLEX_34_ver4_etube_1",
    "author": "BMC <bmchae3@postech.ac.kr>",
    "description": "PURE_34 proteins delta RF1 and T7RNAP",
}

# requirements
requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

# protocol run function_Trial 1
def run(protocol: protocol_api.ProtocolContext):
    # load tip rack
    tiprack1 = protocol.load_labware(
        load_name="opentrons_96_tiprack_20ul", location=9
    )
   
    tiprack2 = protocol.load_labware(
        load_name="opentrons_96_tiprack_300ul", location=4
    )
    
    # attach pipette to right mount
    p20 = protocol.load_instrument(
        instrument_name="p20_single_gen2",
        mount="right",
        tip_racks=[tiprack1]
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
    
    # load well plate in deck slot 6
    dna_plate = protocol.load_labware(
        load_name="chbpcrstrip_96_aluminumblock_200ul", location=8
    )
    
    # Load temperature module in deck slot 10
    reaction_plate1 = protocol.load_labware(
        load_name="axygen_24_aluminumblock_1500ul", location=5
    )
    reaction_plate2 = protocol.load_labware(
        load_name="axygen_24_aluminumblock_1500ul", location=6
    )

    # Mixtures
    p300.transfer(
    300,
    rack["C1"],
    rack["B3"],
    mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    300,
    rack["C1"],
    rack["B3"],
    mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    300,
    rack["C1"],
    rack["B3"],
    mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    150,
    rack["C1"],
    rack["B3"],
    mix_before=(3, 100),
    new_tip='always'
    )
    p300.transfer(
    300,
    rack["C2"],
    rack["B3"],
    mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    162,
    rack["C2"],
    rack["B3"],
    mix_before=(3, 100),
    new_tip='always'
    )
    p300.transfer(
    300,
    rack["B1"],
    rack["B3"],
    mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    141,
    rack["B1"],
    rack["B3"],
    mix_before=(3, 300),
    new_tip='always'
    )  
    p300.transfer(
    300,
    rack["B2"],
    rack["B3"],
    #mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    300,
    rack["B2"],
    rack["B3"],
    #mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    300,
    rack["B2"],
    rack["B3"],
    #mix_before=(3, 300),
    new_tip='always'
    )
    p300.transfer(
    87,
    rack["B2"],
    rack["B3"],
    #mix_before=(3, 50),
    mix_after=(10,300),
    new_tip='always'
    )
    
    # Transfering reaction mixture
    target_wells = (
    [reaction_plate1[f"{row}{col}"] for row in ["A","B","C","D"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["A"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["B"] for col in [1,2,3]]
    )

    chunk_size = 7
    chunks = [
    target_wells[i : i + chunk_size]
    for i in range(0, len(target_wells), chunk_size)
    ]  

    p300.pick_up_tip()
    for group in chunks:
        p300.mix(5, 300, rack["B3"])
        p300.aspirate(300, rack["B3"])
        for well in group:
            p300.dispense(42, well)
        leftover = 300 - 42 * len(group)
        if leftover > 0:
            p300.dispense(leftover, rack["B3"])

    p300.drop_tip()

    # Transfering DNA template
    dna_sources1 = (
    [dna_plate[f"{row}{col}"] for row in ["A","B","C","D","E","F","G","H"] for col in [1,3,5,7]]
    + [dna_plate[f"{row}{col}"] for row in ["A"] for col in [9]]
    )
    
    dna_targets = (
    [reaction_plate1[f"{row}{col}"] for row in ["A","B","C","D"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["A"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["B"] for col in [1,2,3]]
    )
    
    p20.transfer(
    3,                                                                         # Volume(µL)
    dna_sources1,                                                               
    dna_targets,                                                               # A1-12 of temp_combo
    mix_after=(2, 20),
    new_tip='always'                                                           # Different pipet tip  
    )
   
    protocol.delay(seconds=5*60)                                               # etube 교체시간 5분
    
    # Transfering reaction mixture
    target_wells_EFTu = (
    [reaction_plate1[f"{row}{col}"] for row in ["A","B","C","D"] for col in [1,2,3,4,5,6]]
    + [reaction_plate2[f"{row}{col}"] for row in ["A"] for col in [1,2,3,4,5,6]]
    )
    
    chunk_size = 7
    chunks = [
    target_wells_EFTu[i : i + chunk_size]
    for i in range(0, len(target_wells), chunk_size)
    ]  

    p300.pick_up_tip()
    for group in chunks:
        p300.mix(5, 300, rack["B3"])
        p300.aspirate(300, rack["B3"])
        for well in group:
            p300.dispense(42, well)
        leftover = 300 - 42 * len(group)
        if leftover > 0:
            p300.dispense(leftover, rack["B3"])

    p300.drop_tip()
        
    p20.transfer(
    3,                                                                         # Volume(µL)
    dna_plate["B9"],                                                            
    target_wells_EFTu,                                                              
    mix_after=(2, 20),
    new_tip='always'                                                           # Different pipet tip  
    )