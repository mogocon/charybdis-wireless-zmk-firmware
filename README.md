# ZMK Firmware Configuration for Charybdis 4x6 Split Keyboard

This repository contains the ZMK firmware configuration for a Charybdis 4x6 split keyboard with PMW3610 trackball sensor and nRF52840 Nano board.

## Features

- Support for Charybdis 4x6 split keyboard layout
- PMW3610 trackball integration
- Bluetooth functionality using nRF52840 Nano board
- Compatible with BastardKB Splinky adapter v2 and v3
- Multiple keyboard layers
- Customizable keymap

## Prerequisites

To build and flash the firmware, you need to set up the ZMK development environment:

1. Install the required dependencies based on your operating system:
   - [ZMK Setup Guide](https://zmk.dev/docs/development/setup)

2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/zmk-config-charybdis.git
   cd zmk-config-charybdis
   ```

## Building the Firmware

1. Initialize and update the workspace:
   ```bash
   west init -l config
   west update
   ```

2. Build the firmware for your specific board and version:
   ```bash
   # For Splinky v2 left half
   west build -p -b charybdis_left -d build/left_splinky_v2 -- -DSHIELD=splinky_v2_left
   
   # For Splinky v2 right half
   west build -p -b charybdis_right -d build/right_splinky_v2 -- -DSHIELD=splinky_v2_right

   # For Splinky v3 left half
   west build -p -b charybdis_left -d build/left_splinky_v3 -- -DSHIELD=splinky_v3_left
   
   # For Splinky v3 right half
   west build -p -b charybdis_right -d build/right_splinky_v3 -- -DSHIELD=splinky_v3_right
   ```

3. The compiled firmware will be available at:
   - `build/left_splinky_v2/zephyr/zmk.uf2` (for Splinky v2 left half)
   - `build/right_splinky_v2/zephyr/zmk.uf2` (for Splinky v2 right half)
   - `build/left_splinky_v3/zephyr/zmk.uf2` (for Splinky v3 left half)
   - `build/right_splinky_v3/zephyr/zmk.uf2` (for Splinky v3 right half)

## Flashing the Firmware

1. Connect your nRF52840 Nano board to your computer while pressing the RESET button to enter the bootloader mode.
2. The board should appear as a USB drive.
3. Copy the appropriate `.uf2` file to the USB drive.
4. The board will automatically reset and run the new firmware.

## Customizing the Keymap

To customize the keymap, edit the `config/charybdis.keymap` file. Refer to the [ZMK Keymap Documentation](https://zmk.dev/docs/features/keymaps) for details on how to modify the keymap.

## Trackball Configuration

The PMW3610 trackball sensor is configured in the `config/boards/arm/charybdis/charybdis_pmw3610.dtsi` file. You can adjust the sensitivity and behavior by modifying the parameters in this file.

## Troubleshooting

1. **Connectivity Issues**: If you experience connectivity issues, make sure both halves have been flashed with the correct firmware.
2. **Build Errors**: Ensure you have installed all the prerequisites and that your ZMK environment is set up correctly.
3. **Trackball Not Working**: Verify the PMW3610 sensor connections and make sure the SPI configuration is correct.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
