# Comprehensive RV Fitting Examples

This guide demonstrates all three types of radial velocity likelihoods supported by octofitterpy.

## 1. Absolute Stellar RV

The `StarAbsoluteRVLikelihood` is used for traditional stellar RV measurements from one or more instruments. Each instrument requires its own offset and jitter parameters.

```python
import octofitterpy as octo

# Create RV data for two instruments
sophie_rv = octo.StarAbsoluteRVLikelihood(
    epoch = [50000, 50050, 50100, 50150, 50200, 50250, 50300, 50350, 50400, 50450, 50500, 50550, 50600, 50650, 50700, 50750, 50800, 50850, 50900, 50950, 51000, 51050, 51100, 51150, 51200, 51250, 51300, 51350, 51400, 51450, 51500],
    rv = [-79.36087104722361, -220.5342186382704, -271.26485792632894, -210.74777987705946, -63.80148418248903, 109.31027036394889, 237.59307746592305, 268.4372125434599, 189.1932684936805, 32.35977076411365, -137.7447074329559, -251.35906599436566, -261.88921918659037, -165.0166735829619, -0.46957404321580315, 164.27010127220558, 261.64139745805744, 251.71162836526383, 138.55306547675144, -31.4271306384218, -188.51882887478274, -268.29756608939186, -238.04549421662318, -110.16921087584872, 62.88827774336037, 210.15482020126757, 271.235322146796, 221.08021959583058, 80.25848972542492, -93.4778382508882, -228.87821587028037],
    σ_rv = [150.0] * 31,
    instrument_name = "SOPHIE",
    offset = "rv0_sophie",           # Parameter name for instrument offset
    jitter = "jitter_sophie"         # Parameter name for instrument jitter
)

harps_rv = octo.StarAbsoluteRVLikelihood(
    epoch = [51200, 51250, 51300, 51350, 51400, 51450, 51500, 51550, 51600, 51650, 51700, 51750, 51800, 51850, 51900, 51950, 52000, 52050, 52100, 52150, 52200, 52250, 52300, 52350, 52400, 52450, 52500],
    rv = [162.88827774336036, 310.15482020126757, 371.235322146796, 321.0802195958306, 180.2584897254249, 6.5221617491118025, -128.87821587028037, -170.4139504302778, -101.05093108788736, 50.76455674988727, 222.77186270789758, 344.4295229952228, 365.84483456497173, 278.2352203210602, 117.53002870890859, -50.36435686528159, -156.593211570393, -157.59129923225777, -52.949296745307095, 114.41833950542244, 275.87290846820736, 365.20070156279814, 345.7677325348949, 225.54360519518457, 53.833120164239254, -98.943987216648, -170.13269931098864],
    σ_rv = [100.0] * 27,
    instrument_name = "HARPS",
    offset = "rv0_harps",
    jitter = "jitter_harps"
)

# Planet model with absolute RV
planet_b = octo.Planet(
    name="b",
    basis="RadialVelocityOrbit",
    priors="""
        P_days ~ Uniform(50, 3000)
        e ~ Uniform(0.0, 0.5)          # Eccentricity
        ω ~ UniformCircular()          # Argument of periastron (rad)
        τ ~ UniformCircular(1.0)
        mass ~ LogUniform(1, 1000)     # Mass (Jupiter masses)

        P_kep_yrs = b.P_days/PlanetOrbits.kepler_year_to_julian_day_conversion_factor
        a = ∛(system.M * b.P_kep_yrs^2)
        tp =  b.τ*b.P_days + 54899.5
    """,
    likelihoods=[]
)

# System model with parameters for both instruments
system = octo.System(
    name="absolute_rv_example",
    priors="""
        M ~ truncated(Normal(1.0, 0.1), lower=0)   # Total system mass (Msun)
        
        # SOPHIE instrument parameters
        rv0_sophie ~ Normal(0, 5000)    # Zero-point offset (m/s)
        jitter_sophie ~ truncated(Normal(0, 5000), lower=0)  # Jitter (m/s)
        
        # HARPS instrument parameters  
        rv0_harps ~ Normal(0, 5000)     # Zero-point offset (m/s)
        jitter_harps ~ truncated(Normal(0, 5000), lower=0)   # Jitter (m/s)
    """,
    likelihoods=[sophie_rv, harps_rv],
    companions=[planet_b]
)

model = octo.LogDensityModel(system)
chain = octo.octofit(model)

# General orbit plot
octo.octoplot(model, chain)
octo.octocorner(model, chain)

# RV-specific visualization
octo.rvpostplot(model, chain)
```



## 2. Marginalized Absolute RV

The `MarginalizedStarAbsoluteRVLikelihood` automatically marginalizes out the zero-point offset, requiring one less parameter per instrument:

```python
# Same data, but with marginalized offset
sophie_rv_marg = octo.MarginalizedStarAbsoluteRVLikelihood(
    epoch = [50000, 50050, 50100, 50150, 50200, 50250, 50300, 50350, 50400, 50450, 50500, 50550, 50600, 50650, 50700, 50750, 50800, 50850, 50900, 50950, 51000, 51050, 51100, 51150, 51200, 51250, 51300, 51350, 51400, 51450, 51500],
    rv = [-79.36087104722361, -220.5342186382704, -271.26485792632894, -210.74777987705946, -63.80148418248903, 109.31027036394889, 237.59307746592305, 268.4372125434599, 189.1932684936805, 32.35977076411365, -137.7447074329559, -251.35906599436566, -261.88921918659037, -165.0166735829619, -0.46957404321580315, 164.27010127220558, 261.64139745805744, 251.71162836526383, 138.55306547675144, -31.4271306384218, -188.51882887478274, -268.29756608939186, -238.04549421662318, -110.16921087584872, 62.88827774336037, 210.15482020126757, 271.235322146796, 221.08021959583058, 80.25848972542492, -93.4778382508882, -228.87821587028037],
    σ_rv = [150.0] * 31,
    instrument_name = "SOPHIE",
    jitter = "jitter_sophie"         # Only jitter needed, offset is marginalized
)

harps_rv_marg = octo.MarginalizedStarAbsoluteRVLikelihood(
    epoch = [51200, 51250, 51300, 51350, 51400, 51450, 51500, 51550, 51600, 51650, 51700, 51750, 51800, 51850, 51900, 51950, 52000, 52050, 52100, 52150, 52200, 52250, 52300, 52350, 52400, 52450, 52500],
    rv = [162.88827774336036, 310.15482020126757, 371.235322146796, 321.0802195958306, 180.2584897254249, 6.5221617491118025, -128.87821587028037, -170.4139504302778, -101.05093108788736, 50.76455674988727, 222.77186270789758, 344.4295229952228, 365.84483456497173, 278.2352203210602, 117.53002870890859, -50.36435686528159, -156.593211570393, -157.59129923225777, -52.949296745307095, 114.41833950542244, 275.87290846820736, 365.20070156279814, 345.7677325348949, 225.54360519518457, 53.833120164239254, -98.943987216648, -170.13269931098864],
    σ_rv = [100.0] * 27,
    instrument_name = "HARPS",
    jitter = "jitter_harps"
)

# System model needs only jitter parameters
system = octo.System(
    name="marginalized_rv_example",
    priors="""
        M ~ truncated(Normal(1.0, 0.1), lower=0)    # Total system mass (Msun)
        
        # Only jitter parameters needed
        jitter_sophie ~ truncated(Normal(0, 5000), lower=0)  # Jitter (m/s)
        jitter_harps ~ truncated(Normal(0, 5000), lower=0)   # Jitter (m/s)
    """,
    likelihoods=[sophie_rv_marg, harps_rv_marg],
    companions=[planet_b]  # Can reuse same planet model
)

model = octo.LogDensityModel(system)
chain = octo.octofit(model)

# General orbit plot
octo.octoplot(model, chain)
octo.octocorner(model, chain)

# RV-specific visualization
octo.rvpostplot(model, chain)
```

## 3. Relative RV

The `PlanetRelativeRVLikelihood` is used when measuring the RV difference between star and planet directly:

```python
relative_rv = octo.PlanetRelativeRVLikelihood(
    epoch =[51200, 51250, 51300, 51350, 51400, 51450, 51500, 51550, 51600, 51650, 51700, 51750, 51800, 51850, 51900, 51950, 52000, 52050, 52100, 52150, 52200, 52250, 52300, 52350, 52400, 52450, 52500],
    # Relative RV (planet - star) in m/s
    rv = [-6294.894001378374, -21035.753633520035, -27149.695676378436, -22129.34744113164, -8033.590736798406, 9356.800732700296, 22909.899266244825, 27067.479274900365, 20124.48655759695, 4928.293594477741, -12289.028891073242, -24466.530063702598, -26610.126949726306, -17840.71466882952, -1754.6938240863158, 15050.939889227782, 25684.072235217343, 25783.977277316953, 15309.683221508243, -1443.224749020941, -17604.25561404998, -26545.65151619608, -24600.48010186783, -12566.470503129956, 4621.141258255704, 19913.588933870786, 27039.327033382175],
    σ_rv = [200.0] * 27,
    instrument_name = "CRIRES",
    jitter = "jitter_crires"           # Only jitter parameter needed
)

# Planet model for relative RV
planet_rel = octo.Planet(
    name="b",
    basis="RadialVelocityOrbit",
    priors="""
        P_days ~ Uniform(50, 3000)
        e ~ Uniform(0.0, 0.5)          # Eccentricity
        ω ~ UniformCircular()          # Argument of periastron (rad)
        τ ~ UniformCircular(1.0)

        P_kep_yrs = b.P_days/PlanetOrbits.kepler_year_to_julian_day_conversion_factor
        a = ∛(system.M * b.P_kep_yrs^2)
        tp =  b.τ*b.P_days + 54899.5

        jitter_crires ~ truncated(Normal(0, 5000), lower=0)  # Jitter (m/s)
    """,
    likelihoods=[relative_rv]          # Attach relative RV to planet
)

# System model for relative RV
system = octo.System(
    name="relative_rv_example", 
    priors="""
        M ~ truncated(Normal(1.0, 0.1), lower=0)   # Total system mass (Msun)
    """,
    likelihoods=[],
    companions=[planet_rel]
)


model = octo.LogDensityModel(system)
chain = octo.octofit(model)

# General orbit plot
octo.octoplot(model, chain)
octo.octocorner(model, chain)

```

Key differences between the three RV types:

1. `StarAbsoluteRVLikelihood`:
   - Traditional stellar RV measurements
   - Requires offset and jitter parameters for each instrument
   - Attached to system model via `likelihoods`

2. `MarginalizedStarAbsoluteRVLikelihood`:
   - Same as absolute RV but marginalizes out the offset
   - Only requires jitter parameter for each instrument
   - Can improve sampling efficiency
   - Attached to system model via `likelihoods`

3. `PlanetRelativeRVLikelihood`:
   - For direct RV measurements of planet-star difference
   - Only requires jitter parameter
   - Attached to planet model via `likelihoods`

Notes:
- All three types can be mixed in the same model
- When using multiple instruments, each must have unique parameter names
- The choice of RV model affects what system parameters are needed
- `rvpostplot()` works with stellar RVs, but not relative RVs

