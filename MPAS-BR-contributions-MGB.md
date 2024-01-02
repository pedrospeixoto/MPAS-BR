!----------------------------------------------------
!   Modifications made by Marta Gil Bardaji
!   Date: July 2022
!
!   Features:
!   - Add an fdda (four-dimensional data assimilation) scheme of analysis
!     nudging, based on the implementation for MPAS v4 described in:
!       https://gmd.copernicus.org/articles/11/2897/2018/
!       Bullock Jr., O. R., Foroutan, H., Gilliam, R. C., and Herwehe, J. A.:
!       Adding four-dimensional data assimilation by analysis nudging to
!       the Model for Prediction Across Scales – Atmosphere (version 4.0),
!       Geosci. Model Dev., 11, 2897–2922,
!       https://doi.org/10.5194/gmd-11-2897-2018, 2018.
!
!   Based on MPAS version 7.2 (Feb 2022), with PXT modifications
!   (see PXT_modifications_to_MPAS.txt)
!
!
!   As of July 21st 2022 the changes can be seen by comparing GitHub branches:
!
!       https://github.com/marta-gil/MPAS-PXT-MGB/compare/master...marta-gil:MPAS-PXT-MGB:mpas-nudging
!
!   which will compare the branch that has nudging (marta-gil:MPAS-PXT-MGB:mpas-nudging)
!   with the reference branch
!
!
! Marta Gil Bardaji DISCLAIMER:
!   This is a very first version of the code. It compiles and
!   runs in my system (namelist config_fdda_scheme='analysis', regional MPAS,
!   only one CORE) but has not been tested in general environments.
!   I was neither familiar with Fortran nor MPAS code before doing this,
!   so I expect many errors to be found. The idea is that someone that knows
!   more than I do can do their job more easily having these notes as reference.
!
!   Contact: marta.gil@vortexfdc.com

###################
##### SUMMARY #####

Cores changed:

    * init_atmosphere

        - Modify the Registry file so that extra variables are included
          in init.nc files

    * atmosphere

        - Modify the Registry file
            Add package "fdda_in", add stream "fdda", add var_struct "fdda_in",
            add variables to the restart files, add config options for the
            namelist, add variables to the "tend_physics" structure.
        - Update Makefile
        - Add the mpas_atmphys_fdda.F file
        - Update the control, driver, manager, packages, to_dynamics files

This is surely not fully version 7 compliant: I did neither add a
mpas_atmphys_driver_fdda file nor added information on the
mpas_atmphys_vars. My guess is that most of that logic must be
already included in mpas_atmphys_fdda.F.



--------------------------------------
        INIT_ATMOSPHERE_MODEL
--------------------------------------

1. Registry.xml

    - Add wind variables and pressure in the init.nc creation (line 574-575)

        This is needed so that we can generate the fdda files from
        era5 input in a way that they include variables 'uReconstructZonal'
        and 'uReconstructMeridional' (that are used in fdda).

        In my case, I also added the 'pressure' variable on the init.nc
        files because it is useful for me in the post-processing of the
        fdda files for external analysis in order to obtain the temperature
        from the potential temperature. This addition is not essential.

            <stream name="output"
                    type="output"
                    filename_template="x1.40962.init.nc"
                    output_interval="initial_only"
                    packages="initial_conds"
                    immutable="true">

                    <var name="initial_time" packages="met_stage_out"/>
                    ...
                    <var name="uReconstructZonal" packages="met_stage_out"/>
                    <var name="uReconstructMeridional" packages="met_stage_out"/>
                    <var name="pressure" packages="met_stage_out"/>
                    ...


--------------------------------------
        ATMOSPHERE_MODEL: Registry.xml
--------------------------------------

## 1. Registry.xml

    - Add "fdda_in" to the packages list (line 386)
        I called it 'Analysis Nudging' but it
        could be renamed to something more general if other kind of
        fdda (spectral, observations) plan to be implemented.

            <package name="fdda_in" description="Analysis nudging"/>

    - Add fdda values in the restart files (lines 804-815)

        <stream name="restart"
                        type="input;output"
                        filename_template="restart.$Y-$M-$D_$h.$m.$s.nc"
                        input_interval="initial_only"
                        output_interval="1_00:00:00"
                        immutable="true">
            ...
            <var name="rthfddaten"/>
            <var name="rqvfddaten"/>
            <var name="rufddaten"/>
            <var name="rvfddaten"/>
            <var name="th_fdda_old"/>
            <var name="qv_fdda_old"/>
            <var name="u_fdda_old"/>
            <var name="v_fdda_old"/>
            <var name="th_fdda_new"/>
            <var name="qv_fdda_new"/>
            <var name="u_fdda_new"/>
            <var name="v_fdda_new"/>
            ...

    - Add a stream called fdda (lines 864-874)
        The input files for fdda are expected to have their variables
        named in this specific way. Therefore, the output variables from
        the init_atmosphere output will have to be renamed
        {
        'qv': 'qv_fdda_new',
        'theta': 'th_fdda_new',
        'uReconstructZonal': 'u_fdda_new',
        'uReconstructMeridional': 'v_fdda_new',
        }

        <stream name="fdda"
                type="input"
                filename_template="x1.40962.fdda.nc"
                input_interval="1:00:00"
                immutable="true">
                <var name="qv_fdda_new"/>
                <var name="th_fdda_new"/>
                <var name="u_fdda_new"/>
                <var name="v_fdda_new"/>
        </stream>

        NOTE: I left the stream definition as it was in the version 4 code
        by default. However, when I have run the cases, I have used separate
        fdda files for each timestamp. In particular, I run init_atmosphere
        for each timestamp to get a 'init.nc' file, and then I store only the
        variables needed for fdda renamed to their expected names. Then, the
        streams.atmosphere file for my case (hourly fdda) looks like:

            <immutable_stream name="fdda"
                      type="input"
                      filename_template="fdda.$Y-$M-$D_$h.nc"
                      filename_interval="input_interval"
                      input_interval="1:00:00" />

    - Add var_struct called fdda (lines 1529-1539)

        <var_struct name="fdda" time_levs="1" packages="fdda_in">
                <var name="qv_fdda_new"  type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="th_fdda_new"  type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="u_fdda_new"   type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="v_fdda_new"   type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="qv_fdda_old"  type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="th_fdda_old"  type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="u_fdda_old"   type="real"  dimensions="nVertLevels nCells Time"/>
                <var name="v_fdda_old"   type="real"  dimensions="nVertLevels nCells Time"/>
        </var_struct>


    - Add config options for the namelist (lines 2020 - 2084)
        In v7 you need units, description and possible values.

        NOTE: This needs revision. I put the values to the best of my knowledge,
        adding (?) to places I wasn't completely sure (in many cases, those
        are scaled nudging options, which is implemented but not fully explained
        in the reference code for MPAS v4 I am looking at)

            <nml_option name="config_fdda_scheme"                type="character"     default_value="off"        in_defaults="false" units="-"
                 description="configuration for nudging: scaled / analysis / off"
                 possible_values="`scaled',`analysis',`off'"/>
            <nml_option name="config_fdda_int"                   type="real"          default_value="21600."     in_defaults="false"
                 units="(?)"
                 description="config_fdda_int (?)"
                 possible_values="Possitive reals (?)"/>
            <nml_option name="config_fdda_scale_min"             type="real"          default_value="0."         in_defaults="false"
                 units="(?)"
                 description="config_fdda_scale_min (?)"
                 possible_values="Possitive reals (?)"/>
            <nml_option name="config_fdda_scale_max"             type="real"          default_value="100000."    in_defaults="false"
                 units="(?)"
                 description="config_fdda_scale_max"
                 possible_values="Possitive reals (?)"/>
            <nml_option name="config_fdda_t"                     type="logical"       default_value="false"      in_defaults="false"
                 units="-"
                 description="Activate temperature nudging"
                 possible_values="`true',`false'"/>
            <nml_option name="config_fdda_t_coef"                type="real"          default_value="3.0e-4"     in_defaults="false"
                 units="(?)"
                 description="Nudging coefficient for t"
                 possible_values="Real. Recommended order e-4"/>
            <nml_option name="config_fdda_t_in_pbl"              type="logical"       default_value="true"       in_defaults="false"
                 units="-"
                 description="Activate temperature nudging in pbl"
                 possible_values="`true',`false'"/>
            <nml_option name="config_fdda_t_min_layer"           type="integer"       default_value="0"          in_defaults="false"
                 units="-"
                 description="config_fdda_t_min_layer"
                 possible_values="Positive integers (?)"/>
            <nml_option name="config_fdda_q"                     type="logical"       default_value="false"      in_defaults="false"
                 units="-"
                 description="Activate humidity nudging"
                 possible_values="`true',`false'"/>
            <nml_option name="config_fdda_q_coef"                type="real"          default_value="3.0e-4"     in_defaults="false"
                 units="-"
                 description="Nudging coefficient for q"
                 possible_values="Real. Recommended order e-4"/>
            <nml_option name="config_fdda_q_in_pbl"              type="logical"       default_value="true"       in_defaults="false"
                 units="-"
                 description="Activate humidity nudging in pbl"
                 possible_values="`true',`false'"/>
            <nml_option name="config_fdda_q_min_layer"           type="integer"       default_value="0"          in_defaults="false"
                 units="-"
                 description="config_fdda_q_min_layer"
                 possible_values="Positive integers (?)"/>
            <nml_option name="config_fdda_uv"                    type="logical"       default_value="false"      in_defaults="false"
                 units="-"
                 description="Activate wind nudging"
                 possible_values="`true',`false'"/>
            <nml_option name="config_fdda_uv_coef"               type="real"          default_value="3.0e-4"     in_defaults="false"
                 units="-"
                 description="Nudging coefficient for wind"
                 possible_values="Real. Recommended order e-4"/>
            <nml_option name="config_fdda_uv_in_pbl"             type="logical"       default_value="true"       in_defaults="false"
                 units="-"
                 description="Activate wind nudging in the pbl"
                 possible_values="`true',`false'"/>
            <nml_option name="config_fdda_uv_min_layer"          type="integer"       default_value="0"          in_defaults="false"
                 units="-"
                 description="config_fdda_uv_min_layer"
                 possible_values="Positive integers (?)"/>

    - In "tend_physics" add tendencies for the 4 variables (lines 2962 - 2978)

        <var_struct name="tend_physics" time_levs="1">
            <!-- ================================================================================================== -->
            <!-- ================================================================================================== -->
            <!-- TENDENCIES FROM FOUR DIMENSIONAL DATA ASSIMILATION:                                                -->
            <!-- ================================================================================================== -->
            <var name="rthfddaten"    type="real"     dimensions="nVertLevels nCells Time" units="K s^{-1}"
                 description="tendency of potential temperature due to fdda"
                 packages="fdda_in"/>
            <var name="rqvfddaten"    type="real"     dimensions="nVertLevels nCells Time" units="kg/kg s^{-1}"
                 description="tendency of water vapor mixing ratio due to fdda"
                 packages="fdda_in"/>
            <var name="rufddaten"     type="real"     dimensions="nVertLevels nCells Time" units="m s^{-1}"
                 description="tendency of zonal wind due to fdda "
                 packages="fdda_in"/>
            <var name="rvfddaten"     type="real"     dimensions="nVertLevels nCells Time" units="m s^{-1}"
                 description="tendency of meridional wind due to fdda"
                 packages="fdda_in"/>

    - In "tend_physics", add _Edge variables for fdda and include packages for other Edge
    variables in Registry (lines 2980-2983, 3031-3034, 3069-72)
        The _Edge tendencies not needed in v4, but it I added it in v7
        analogously for other physics parametrizations.

            <var name="rufddaten_Edge"    type="real"     dimensions="nVertLevels nEdges Time" units="m s^{-1} s^{-1}"
                 description="tendency of wind in edges due to fdda"
                 packages="fdda_in"/>

            <!-- MGD should we add packages to the field below? -->
            <var name="rucuten_Edge" type="real"     dimensions="nVertLevels nEdges Time" units="m s^{-1} s^{-1}"
                     description="tendency of wind in edges due to cumulus convection"
                     packages="cu_grell_freitas_in;cu_tiedtke_in"/>

            <!-- MGD should we add packages to the field below? -->
            <var name="rublten_Edge" type="real"     dimensions="nVertLevels nEdges Time" units="m s^{-1} s^{-1}"
                     description="tendency of wind in edges due to pbl processes"
                     packages="bl_mynn_in;bl_ysu_in"/>


## 2. physics' Makefile:

    - Added mpas_atmphys_fdda to the needed places (line 24, 76, 98-102)

        OBJS = \
            ...
            mpas_atmphys_fdda.o                \
            ...


        mpas_atmphys_driver.o: \
            ...
            mpas_atmphys_fdda.o \
            ...

        mpas_atmphys_fdda.o: \
            mpas_atmphys_constants.o \
            mpas_atmphys_utilities.o \
            mpas_atmphys_vars.o \


## 3. Main routine: mpas_atmphys_fdda.F

    I have used as reference the file designed for version 4 and
    made changes to adapt to version 7 based on analogy with the differences
    between version 4 and 7 for other packages.

    - remove  use mpas_derived_types form line 4 and add some other imports:

         module mpas_atmphys_fdda
         use mpas_kind_types
         use mpas_pool_routines
         use mpas_timer, only : mpas_timer_start, mpas_timer_stop

    - add the fdda_scheme variable definition
        (line 88)
            character(len=StrKIND),pointer:: config_fdda_scheme
        (line 107)
             call mpas_pool_get_config(configs,'config_fdda_scheme',config_fdda_scheme)

    - change fdda_scheme to config_fdda_scheme (line 161)

         fdda_select: select case(config_fdda_scheme)

    - change write(0,*) MESSAGE to call mpas_log_write(MESSAGE)

    - add mpas timer start and stop for FDDA


## 4. Update other mpas_atmphys files

* mpas_atmphys_control.F

    - Add config_fdda_scheme in local pointers (line 98)

    - Add in line 114
         call mpas_pool_get_config(configs,'config_fdda_scheme',
                config_fdda_scheme)

    - Add control for fdda scheme logic 166-173

        !fdda scheme:
         if(.not. (config_fdda_scheme .eq. 'off'        .or. &
                   config_fdda_scheme .eq. 'analysis'   .or. &
                   config_fdda_scheme .eq. 'scaled'     )) then
            write(mpas_err_message,'(A,A10)') 'illegal value for config_fdda_scheme:', &
                  trim(config_fdda_scheme)
            call physics_error_fatal(mpas_err_message)
         endif

    - Add log (line 321)

        call mpas_log_write('    config_fdda_scheme         = '//trim(config_fdda_scheme))


* mpas_atmphys_driver.F

    - Add fdda to header line 22
        use mpas_atmphys_fdda

    - Add comment line 72
        ! apply_fdda                  : applies four-dimensional data assimilation.

    - Add to local pointers line 122
        type(mpas_pool_type),pointer:: configs, &
                                       ...
                                       fdda,         &
                                       ...

    - Add to local pointers line 133
        character(len=StrKIND),pointer:: config_bucket_update, &
                                         ...
                                         config_fdda_scheme,       &
                                         ...

    - Add call line 160
         call mpas_pool_get_config(domain%configs,'config_fdda_scheme'      ,config_fdda_scheme      )

    - Add check if fdda scheme is on line 177-178
         config_sfclayer_scheme   .ne. 'off' .or. &
         config_fdda_scheme       .ne. 'off') then

    - Add call in block (line 185)
        call mpas_pool_get_subpool(block%structs,'fdda'        ,fdda        )

    - Call FDDA. Add in lines (342-348)

        !call to FDDA scheme within MPAS physics (not WRF physics)
        if(config_fdda_scheme .ne. 'off') then
           time_lev = 1
           do thread=1,nThreads
                call apply_fdda(xtime_s,block%configs,mesh,state,time_lev,fdda,diag,diag_physics,tend_physics)
           end do
        endif

        COMMENT: That is not the structure in version 7.2! So maybe it won't work
        in some cases without adding the parallelization like !$OMP PARALLEL DO

        For example, for the scheme PBL:

            v4:

                !call to pbl schemes:
                if(config_pbl_scheme .ne. 'off' .and. config_sfclayer_scheme .ne. 'off') then
                   call allocate_pbl
                   call driver_pbl(sfc_input,diag_physics,tend_physics)
                   end do
                   call deallocate_pbl

                endif

            v7:

                !call to pbl schemes:
                if(config_pbl_scheme .ne. 'off' .and. config_sfclayer_scheme .ne. 'off') then
                   call allocate_pbl(block%configs)
            !$OMP PARALLEL DO
                   do thread=1,nThreads
                      call driver_pbl(itimestep,block%configs,mesh,sfc_input,
                                      diag_physics,tend_physics, &
                                      cellSolveThreadStart(thread),cellSolveThreadEnd(thread))
                   end do
            !$OMP END PARALLEL DO
                   call deallocate_pbl(block%configs)

                endif


* mpas_atmphys_manager.F

    - add in local pointer (line 386)

          config_fdda_scheme,            &

    - add in get config (line 423)

         call mpas_pool_get_config(configs,'config_fdda_scheme'      ,config_fdda_scheme      )


* mpas_atmphys_todynamics.F

    - add pointer to local variables line 83

        config_fdda_scheme

    - line 100
         real(kind=RKIND),dimension(:,:),pointer:: rthfddaten,rqvfddaten,rufddaten,rvfddaten

    - add rufddaten_Edge to allocatable list in line 111
        real(kind=RKIND),dimension(:,:),allocatable:: rublten_Edge,rucuten_Edge,rufddaten_Edge

    - add mpas_pool_get_config (line 126)

        call mpas_pool_get_config(configs, 'config_fdda_scheme', config_fdda_scheme)

    - add mpas_pool_get_array for fdda vars (167-171)

         call mpas_pool_get_array(tend_physics, 'rthfddaten', rthfddaten)
         call mpas_pool_get_array(tend_physics, 'rqvfddaten', rqvfddaten)
         call mpas_pool_get_array(tend_physics, 'rufddaten', rufddaten)
         call mpas_pool_get_array(tend_physics, 'rvfddaten', rvfddaten)
         call mpas_pool_get_array(tend_physics, 'rufddaten_Edge', rufddaten_Edge)

    - allocate if necessary (215-218)

         if (.not. associated(rthfddaten)) allocate(rthfddaten(0,0))
         if (.not. associated(rqvfddaten)) allocate(rqvfddaten(0,0))
         if (.not. associated(rufddaten)) allocate(rufddaten(0,0))
         if (.not. associated(rvfddaten)) allocate(rvfddaten(0,0))

    - add to physics_get_tend_work (line 223)

         call physics_get_tend_work(block, mesh, nCells, nEdges, nCellsSolve, nEdgesSolve, &
                               rk_step, dynamics_substep, &
                               config_pbl_scheme, config_convection_scheme, config_radt_lw_scheme, config_radt_sw_scheme, &
                               config_fdda_scheme, rthfddaten, rqvfddaten, rufddaten, rvfddaten, rufddaten_Edge, &
                               ...

    - clean the allocated vars before physics_get_tend_work (257-260)

         if (size(rthfddaten) == 0) deallocate(rthfddaten)
         if (size(rqvfddaten) == 0) deallocate(rqvfddaten)
         if (size(rufddaten) == 0) deallocate(rufddaten)
         if (size(rvfddaten) == 0) deallocate(rvfddaten)

    - define subroutine physics_get_tend_work (line 286)

            subroutine physics_get_tend_work(block, mesh, nCells, nEdges, nCellsSolve, nEdgesSolve, &
                                 rk_step, dynamics_substep, &
                                 config_pbl_scheme, config_convection_scheme, config_radt_lw_scheme, config_radt_sw_scheme, &
                                 config_fdda_scheme, rthfddaten, rqvfddaten, rufddaten, rvfddaten, rufddaten_Edge, &
                                 ...
    -  add definitions (310-315)

            character(len=StrKIND), intent(in) :: config_fdda_scheme
            real (kind=RKIND), dimension(nVertLevels,nCells+1), intent(in) :: rthfddaten
            real (kind=RKIND), dimension(nVertLevels,nCells+1), intent(in) :: rqvfddaten
            real (kind=RKIND), dimension(nVertLevels,nCells+1), intent(in) :: rufddaten
            real (kind=RKIND), dimension(nVertLevels,nCells+1), intent(in) :: rvfddaten


    - add coupled tendencies 430-447
        We made some modifications on v4 code make it similar to version 7 code
        (the tend_scalars call is different for example)

        !add coupled tendencies due to four-dimensional data assimilation (fdda):
        if(config_fdda_scheme .ne. 'off') then
            call tend_toEdges(block,mesh,rufddaten,rvfddaten,rufddaten_Edge)
            do i = 1, nEdgesSolve
                do k  = 1, nVertLevels
                   tend_u(k,i)=tend_u(k,i)+rufddaten_Edge(k,i)*mass_edge(k,i)
                enddo
            enddo
            do i = 1, nCellsSolve
                do k = 1, nVertLevels
                   tend_th(k,i) = tend_th(k,i) + rthfddaten(k,i)*mass(k,i)
                   tend_scalars(index_qv,k,i) = tend_scalars(index_qv,k,i) + rqvfddaten(k,i)*mass(k,i)
                enddo
            enddo
        endif

* mpas_atmphys_packages.F
    NOTE: In this initialization I completely ignore whether
    config_fdda_scheme=='scaled' or config_fdda_scheme=='analysis'
    and make both cases set fdda_in=true.
    Since I have not tested the 'scaled' version (nor I understand it), it
    has worked fine for my purposes of doing analysis nudging.

    - line 39
        character(len=StrKIND),pointer:: config_fdda_scheme

    - line 43
         logical,pointer:: fdda_in

    - 167-190

         !--- initialization of all packages for analysis nudging:

         call mpas_pool_get_config(configs,'config_fdda_scheme',config_fdda_scheme)

         nullify(fdda_in)
         call mpas_pool_get_package(packages,'fdda_inActive',fdda_in)

         if(.not.associated(fdda_in)) then
            call mpas_log_write('====================================================================================',messageType=MPAS_LOG_ERR)
            call mpas_log_write('* Error while setting up packages for analysis nudging.',  messageType=MPAS_LOG_ERR)
            call mpas_log_write('====================================================================================',messageType=MPAS_LOG_ERR)
            ierr = 1
            return
         endif

         fdda_in = .false.

         if(config_fdda_scheme=='scaled') then
            fdda_in = .true.
         elseif(config_fdda_scheme == 'analysis') then
            fdda_in = .true.
         endif

         call mpas_log_write('    fdda_in                 = $l', logicArgs=(/fdda_in/))
         call mpas_log_write('')

